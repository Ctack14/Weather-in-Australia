import asyncio
from flask import Flask, render_template, request
from practice_data_sets.loader import DataLoader
from practice_data_sets.visualize import DataVisualizer
from practice_data_sets.predictor import RainPredictor, feature_columns
from db import db
from models import RequestLog, Query
import traceback


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
db.init_app(app)

with app.app_context():
    db.create_all()

df_cache = None
predictor_cache = None

async def load_data_once():
    '''Work with async data loading and cache the result to avoid reloading on every request'''

    global df_cache
    if df_cache is None:
        loader = DataLoader(["Weather Training Data.csv"])
        df_cache = await loader.load_files()
    return df_cache

def get_predictor():
    """Train the predictor models and then cache the trained predictor for future use"""
    global predictor_cache
    if predictor_cache is None:
        df = asyncio.run(load_data_once())
        predictor_cache = RainPredictor(df)
        predictor_cache.train()
    return predictor_cache

@app.route("/")
def index():
    df = asyncio.run(load_data_once())

    loactions = sorted(df["Location"].dropna().unique())
    return render_template("index.html", locations=loactions)

@app.route("/analyze", methods = ["POST"])
def analyze():
    location = request.form.get("location")
    graph_type = request.form.get("graph")



    df = asyncio.run(load_data_once())

    if location and location != "ALL":
        df = df[df["Location"] == location]

    visualizer = DataVisualizer(df, output_dir="static")

    image_path = None

    if graph_type == "rain_vs_temp":
        image_path = visualizer.save_rainfall_vs_temperature()
    elif graph_type == "wind_vs_temp":
        image_path = visualizer.save_wind_speed_vs_temp_change()

    log = RequestLog(graph_type=graph_type)
    db.session.add(log)

    new_query = Query(
        location=location,
        graph_type=graph_type,
        image_path=image_path
    )
    db.session.add(new_query)

    db.session.commit()

    return render_template("results.html", image=image_path, location=location)


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    GET: Show prediction form
    POST: run the prediction model and show results
    """
    df = asyncio.run(load_data_once())
    locations = sorted(df["Location"].dropna().unique())

    if request.method == "GET":
        return render_template("predict.html", locations=locations)



    model_choice = request.form.get("model_choice", "random_forest")

    input_data = {}
    for col in feature_columns:
        input_data[col] = request.form.get(col)

    try:
        predictor = get_predictor()
        result = predictor.predict(input_data, model_choice=model_choice)
    except ValueError as e:
        traceback.print_exc()
        return render_template("predict.html", locations=locations, error=str(e))

    metrics = predictor.get_metrics()
    importances = predictor.get_feature_importances()

    return render_template(
        "prediction_results.html",
        result=result,
        metrics=metrics,
        importances=importances,
    )



@app.route("/history")
def history():
    queries = Query.query.order_by(Query.created_at.desc()).all()
    return render_template("history.html", queries=queries)


if __name__ == "__main__":
    app.run(debug=True)

