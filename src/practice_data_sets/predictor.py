import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logger = logging.getLogger(__name__)


feature_columns = [
    "MinTemp",
    "MaxTemp",
    "Rainfall",
    "Evaporation",
    "Sunshine",
    "WindGustSpeed",
    "WindSpeed9am",
    "WindSpeed3pm",
    "Humidity9am",
    "Humidity3pm",
    "Pressure9am",
    "Pressure3pm",
    "Cloud9am",
    "Cloud3pm",
    "Temp9am",
    "Temp3pm",
    "RainToday"
]

target_column = "RainTomorrow"

class RainPredictor:
    """
    Uses scikit-learn classifiers to predict whether it will rain tomorrow.
    """

    def __init__(self, df: pd.DataFrame):
        self.raw_df = df
        self.rf_model = RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)
        self.is_trained = False
        self.metrics = {}
        self.feature_importances = {}

    def _preprocess(selfself, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        """
        Cleans the data for modeling
        """

        logger.info("Preprocessing the data for prediction")

        cols_needed = feature_columns + [target_column]
        data = df[cols_needed].copy()

        for col in ["RainToday", target_column]:
            if data[col].dtype == "boolean" or data[col].dtype == bool:
                data[col] = data[col].astype("Int64")
            elif data[col].dtype == "object":
                data[col] = data[col].map({"Yes": 1, "No": 0, "yes": 1, "no": 0, True: 1, False: 0})

        data = data.dropna()

        data = data.astype(float)

        X = data[feature_columns]
        Y = data[target_column].astype(int)

        logger.info(f"Preprocessed data: {X.shape[0]} rows, {X.shape[1]} features")
        return X, Y

    def train(self, test_size: float = 0.2) -> dict:
        """
        Trains models on weather data.

        Args:
            test_size: The proportion of the dataset to include in the test split.

        Returns:
            A dictionary containing the trained model and its performance metrics.
        """

        logger.info("Training the prediction models")

        X, Y = self._preprocess(self.raw_df)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=42, stratify=Y)

        self.rf_model.fit(X_train, Y_train)
        rf_preds = self.rf_model.predict(X_test)

        self.metrics = {
            "random_forest": self._compute_metrics(Y_test, rf_preds)
        }

        self.feature_importances = dict(
            zip(feature_columns, self.rf_model.feature_importances_)
        )

        self.feature_importances = dict(
            sorted(self.feature_importances.items(), key=lambda x: x[1], reverse=True)
        )

        self.is_trained = True
        logger.info ("Models successfully trained!")
        logger.info (f"Random Forest Accuracy: {self.metrics['random_forest']['accuracy']:.4f}")

        return self.metrics

    def _compute_metrics(self, y_true: pd.Series, y_pred: np.ndarray) -> dict:
        """
        Computes performance metrics for the model.
        """

        return {
            "accuracy": round(accuracy_score(y_true, y_pred), 4),
            "precision": round(precision_score(y_true, y_pred), 4),
            "recall": round(recall_score(y_true, y_pred), 4),
            "f1": round(f1_score(y_true, y_pred), 4)
        }

    def predict(self, input_data: dict, model_choice: str = "random_forest") -> dict:
        """
        Predict whether it will rain tomorrow based on input features using the specified model.

        Args:
            input_data: Dictionary of feature names to values. keys must match the feature_columns list.
            model_choice: Which model to use for prediction. Currently only "random_forest" is supported.

        Returns:
            dict: has a prediction and a confidence score.
        """

        if not self.is_trained:
            raise ValueError("Models haven't been trained yet. Call the train() method before predicting.")

        row = {}
        for col in feature_columns:
            val = input_data.get(col)
            if val is None or val == "":
                raise ValueError(f"Missing value for feature '{col}'")
            row[col] = float(val)

        input_df = pd.DataFrame([row])

        prediction = self.rf_model.predict(input_df)[0]
        probabilities = self.rf_model.predict_proba(input_df)[0]
        confidence = probabilities[int(prediction)]

        result = {
            "prediction": int(prediction),
            "label": "Yes" if prediction == 1 else "No",
            "confidence": round(float(confidence) * 100, 1),
            "probability_rain": round(float(probabilities[1]) * 100, 1),
            "probability_no_rain": round(float(probabilities[0]) * 100, 1),
            "model_used": model_choice
        }

        logger.info(f"Made prediction: {result['label']} (confidence: {result['confidence']}%)")
        return result

    def get_feature_importances(self) -> dict:
        """
        Returns the feature importances for the trained model.
        """
        if not self.is_trained:
            raise ValueError("Models haven't been trained yet. Call the train() method before getting feature importances.")

        return self.feature_importances

    def get_metrics(self) -> dict:
        """
        Returns the performance metrics for the trained model.
        """
        if not self.is_trained:
            raise ValueError("Models haven't been trained yet. Call the train() method before getting metrics.")

        return self.metrics