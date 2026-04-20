
import os
import io
import base64
import asyncio
from flask import Flask, render_template, request, url_for, session, flash, redirect, jsonify
from werkzeug.utils import secure_filename
from practice_data_sets.visualize import DataVisualizer
from practice_data_sets.predictor import RainPredictor, feature_columns
from db import db
from auth import login_required
from models import User, seed_users
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from models import RequestLog, Query
import traceback
import logging


logger = logging.getLogger(__name__)
app = Flask(__name__)
app.secret_key = "super_secret_key_lol"

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db.init_app(app)

with app.app_context():
    db.create_all()
    seed_users()

df_cache = None
predictor_cache = None


#----------------------------------------------------
def get_uploaded_df():
    """Return the DataFrame from cache, or none if there isn't a CSV uploaded yet."""
    return df_cache

def load_csv_to_cache(filepath):
    """Read a csv into the cache from disk"""
    global df_cache, predictor_cache

    raw_df = pd.read_csv(filepath)

    numeric_cols = ["MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine",
        "WindGustSpeed", "WindSpeed9am", "WindSpeed3pm",
        "Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm",
        "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm"]
    for col in numeric_cols:
        if col in raw_df.columns:
            raw_df[col] = pd.to_numeric(raw_df[col], errors="coerce")

    bool_cols = ["RainToday", "RainTomorrow"]
    for col in bool_cols:
        if col in raw_df.columns:
            raw_df[col] = raw_df[col].map({
                "Yes": True, "No": False,
                "yes": True, "no": False,
                1: True, 0: False,
                "1": True, "0": False
            }).astype("boolean")

    df_cache = raw_df
    predictor_cache = None     # Clear the predictor so it can be trained on the new data.
    logger.info(f"Loaded CSV data into cache from {filepath}. {len(raw_df)} rows and {len(raw_df.columns)} columns.")


def get_predictor():
    """Train and subsequently cache the predictor"""
    global predictor_cache
    df = get_uploaded_df()
    if df is None:
        raise ValueError("No data uploaded yet. Please upload a CSV file first.")
    if predictor_cache is None:
        predictor_cache = RainPredictor(df)
        predictor_cache.train()
    return predictor_cache


#------ Auth Routes --------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username").strip()
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect(url_for("upload"))

    flash("Invalid username or password.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


#-------- Upload Route ---------------------------------
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "GET":
        return render_template("upload.html")

    file = request.files.get("file")
    if not file or file.filename == "":
        flash("Please select a CSV file.", "error")
        return render_template("upload.html")

    filename = secure_filename(file.filename)
    if not filename.lower().endswith(".csv"):
        flash("Invalid file type. Please upload a CSV file.", "error")
        return render_template("upload.html")

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        load_csv_to_cache(filepath)
    except Exception as e:
        flash(f"Error processing file: {str(e)}", "error")
        return render_template("upload.html")

    return redirect(url_for("dashboard"))

#-------- Dashboard Route ---------------------------------
@app.route("/")
@login_required
def index():
    """.
    Redirect root to dashboard if data is loaded, else to upload page.
    """
    if get_uploaded_df() is not None:
        return redirect(url_for("dashboard"))
    return redirect(url_for("upload"))

@app.route("/dashboard")
@login_required
def dashboard():
    """Show some basic info about the uploaded dataset and options to visualize or predict."""
    df = get_uploaded_df()
    if df is None:
        return redirect(url_for("upload"))
    return render_template("dashboard.html")


#-------- Cities --------------------------------
@app.route("/api/cities")
@login_required
def api_cities():
    df = get_uploaded_df()
    if df is None:
        return jsonify({"error": "No data uploaded yet"}), 400
    cities = sorted(df["Location"].dropna().unique().tolist())
    return jsonify({"cities": cities})

#-------- Analyze -------------------------------
@app.route("/api/analyze", methods=["POST"])
@login_required
def api_analyze():
    """Returns a JSON object with base64-encoded images for the requested analysis."""
    df = get_uploaded_df()
    if df is None:
        return jsonify({"error": "No data uploaded yet"}), 400

    data = request.get_json()
    category = data.get("category")
    city = data.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    city_df = df[df["Location"] == city]
    if city_df.empty:
        return jsonify({"error": f"No data found for city '{city}'"}), 404

    try:
        if category == "temperature":
            image_b64, summary = _temperature_analysis(city_df, city)
        elif category == "rainfall":
            image_b64, summary = _rainfall_analysis(city_df, city)
        elif category == "prediction":
            image_b64, summary = _prediction_analysis(city_df, city)
        else:
            return jsonify({"error": f"Unknown category: {category}"}), 400

    except Exception as e:
        logger.exception("Error generating analysis")
        return jsonify({"error": str(e)}), 500

    return jsonify({"image": image_b64, "summary": summary})

#------ Prediction --------------------------------
@app.route("/api/prediction-defaults", methods=["POST"])
@login_required
def api_predict():
    df = get_uploaded_df()
    if df is None:
        return jsonify({"error": "No data uploaded yet"}), 400

    data = request.get_json()
    city = data.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    city_df = df[df["Location"] == city]
    if city_df.empty:
        return jsonify({"error": f"No data found for city '{city}'"}), 404

    defaults = {}
    for col in feature_columns:
        if col == "RainToday":
            mode = city_df[col].mode()
            defaults[col] = int(mode.iloc[0]) if not mode.empty else 0
        else:
            median = city_df[col].median()
            defaults[col] = median if not pd.isna(median) else 0.0

    return jsonify({"defaults": defaults, "features": feature_columns})


#------ Chart Generation Functions -------------------------------
def _fig_to_base64(fig):
    """Convert a Matplotlib figure to a base64-encoded PNG."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
    plt.close(fig)
    buf.seek(0)
    image_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return image_b64

def _temperature_analysis(city_df, city):
    """Generate a Min/Max temperature distribution plot and daily range box plot"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left side: histogram of min and max temp
    sns.histplot(city_df["MinTemp"].dropna(), bins=25, kde=True, color="blue", label="MinTemp", ax=axes[0], alpha=0.6)
    sns.histplot(city_df["MaxTemp"].dropna(), bins=25, kde=True, color="red", label="MaxTemp", ax=axes[0], alpha=0.6)
    axes[0].set_title(f"Temperature Distribution — {city}")
    axes[0].set_xlabel("Temperature (°C)")
    axes[0].legend()

    # Right side: box plot of the daily temp range
    temp_range = city_df["MaxTemp"] - city_df["MinTemp"]
    sns.boxplot(y=temp_range.dropna(), ax=axes[1], color="purple")
    axes[1].set_title(f"Daily Temperature Range — {city}")
    axes[1].set_ylabel("Max - Min (°C)")

    fig.tight_layout()
    image_b64 = _fig_to_base64(fig)

    avg_min = city_df["MinTemp"].mean()
    avg_max = city_df["MaxTemp"].mean()
    avg_range = avg_max - avg_min
    record_high = city_df["MaxTemp"].max()
    record_low = city_df["MinTemp"].min()

    summary = (
        f"Over the recorded period, {city} had an average minimum temperature of "
        f"{avg_min:.1f}°C and an average maximum of {avg_max:.1f}°C, "
        f"giving a typical daily swing of about {avg_range:.1f}°C. "
        f"The hottest recorded day reached {record_high:.1f}°C, "
        f"while the coldest morning dropped to {record_low:.1f}°C."
    )
    return image_b64, summary

def _rainfall_analysis(city_df, city):
    """Rainfall distribution and rainfall vs temp scatter plot"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    rainfall = city_df["Rainfall"].dropna()
    rained_only = rainfall[rainfall > 0].reset_index(drop=True)
    rainy_df = pd.DataFrame({"Rainfall": rained_only})
    sns.histplot(data=rainy_df, x="Rainfall", binwidth=2, kde=True, color="blue", ax=axes[0], alpha=0.6)
    axes[0].set_xlim(0, rained_only.quantile(0.95))  # Focus on the bulk of the distribution
    axes[0].set_title(f"Rainfall Distribution (Rainy Days) — {city}")
    axes[0].set_xlabel("Rainfall (mm)")

    temp_rain = city_df[["MaxTemp", "Rainfall"]].dropna().reset_index(drop=True)
    sns.scatterplot(data=temp_rain, x="MaxTemp", y="Rainfall", ax=axes[1], alpha=0.6)
    axes[1].set_title(f"Rainfall vs Max Temperature — {city}")
    axes[1].set_xlabel("Max Temperature (°C)")
    axes[1].set_ylabel("Rainfall (mm)")

    fig.tight_layout()
    image_b64 = _fig_to_base64(fig)

    total_days = len(rainfall)
    rainy_days = int((rainfall > 0).sum())
    pct_rainy = (rainy_days / total_days) * 100 if total_days > 0 else 0
    avg_rainfall = rainfall[rainfall > 0].mean() if rainy_days > 0 else 0
    max_rain = rainfall.max()

    summary = (
        f"Out of {total_days} days with recorded data, {city} saw rain on "
        f"{rainy_days} days ({pct_rainy:.1f}% of the time). "
        f"On days it did rain, the average was {avg_rainfall:.1f} mm, "
        f"with the heaviest single-day rainfall reaching {max_rain:.1f} mm."
    )
    return image_b64, summary

def _prediction_analysis(city_df, city, input_data=None):
    """Run the predictor using the median conditions of the city"""
    predictor = get_predictor()
    metrics = predictor.get_metrics()
    importances = predictor.get_feature_importances()

    if input_data is None:
        input_data = {}
        for col in feature_columns:
            if col == "RainToday":
                mode = city_df[col].mode()
                input_data[col] = int(mode.iloc[0]) if not mode.empty else 0
            else:
                median = city_df[col].median()
                input_data[col] = median if not pd.isna(median) else 0.0

    print("INPUT DATA:", input_data)  # <-- add this
    result = predictor.predict(input_data, model_choice="random_forest")
    print("RESULT:", result)  # <-- and this


    # Feature importance bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    top_features = dict(sorted(importances.items(), key=lambda item: item[1], reverse=True)[:10])
    names = [n.replace("_", " ") for n in top_features.keys()]
    ax.barh(names, [v * 100 for v in top_features.values()], color="teal")
    ax.set_xlabel("Feature Importance (%)")
    ax.set_title(f"Top Feature Importances for Rain Prediction — {city}")
    fig.tight_layout()
    image_b64 = _fig_to_base64(fig)

    rf_metrics = metrics.get("random_forest", {})
    accuracy = rf_metrics.get("accuracy", 0)
    precision = rf_metrics.get("precision", 0)
    recall = rf_metrics.get("recall", 0)

    prediction_label = "Rain" if result["prediction"] == 1 else "No Rain"

    summary = (
        f"Based on {city}'s typical weather conditions, the Random Forest model "
        f"predicts <strong>{prediction_label}</strong> tomorrow "
        f"with {result['confidence']}% confidence. "
        f"The model was trained on the full uploaded dataset and achieves "
        f"{accuracy * 100:.1f}% accuracy, {precision * 100:.1f}% precision, "
        f"and {recall * 100:.1f}% recall on the held-out test set. "
        f"The chart shows which weather features contribute most to the prediction — "
        f"humidity and pressure tend to be the strongest signals."
    )
    return image_b64, summary


if __name__ == "__main__":
    app.run(debug=True)

