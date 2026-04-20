import pytest
import asyncio
from practice_data_sets.loader import DataLoader
from practice_data_sets.predictor import RainPredictor, feature_columns

@pytest.fixture
def weather_df():
    """Load the data once for all tests"""
    async def _load():
        loader = DataLoader(["Weather Training Data.csv"])
        return await loader.load_files()
    return asyncio.run(_load())

@pytest.fixture
def trained_predictor(weather_df):
    """Train the predictor once for all tests"""
    predictor = RainPredictor(weather_df)
    predictor.train()
    return predictor

class TestRainPredictorTraining:
    """Tests for model training and metrics"""

    def test_metrics_return(self, weather_df):
        predictor = RainPredictor(weather_df)
        metrics = predictor.train()

        assert "random_forest" in metrics

    def test_is_trained_flag(self, weather_df):
        predictor = RainPredictor(weather_df)
        assert predictor.is_trained == False
        predictor.train()
        assert predictor.is_trained == True

    def test_metrics_keys(self, trained_predictor):
        """Make sure the expected keys are returned"""
        metrics = trained_predictor.get_metrics()
        expected_keys = {"accuracy", "precision", "recall", "f1"}

        # Extensible to support models in the future (possibly logistic regression next)
        for model_name in ["random_forest"]:
            assert model_name in metrics
            for key in expected_keys:
                assert key in metrics[model_name]

    def test_accuracy_beats_baseline(self, trained_predictor):
        """Check that accuracy is above a reasonable baseline (e.g. 0.8)"""
        metrics = trained_predictor.get_metrics()
        assert metrics["random_forest"]["accuracy"] >= 0.8

class TestRainPredictions:
    """Tests for making predictions"""

    def test_sunny_day(self, trained_predictor):
        """Low humidity, high pressure, no rain today should predict no rain tomorrow"""

        input_data = {
            "MinTemp": 10.0,
            "MaxTemp": 28.0,
            "Rainfall": 0.0,
            "WindGustSpeed": 20.0,
            "WindSpeed9am": 5.0,
            "WindSpeed3pm": 10.0,
            "Humidity9am": 30.0,
            "Humidity3pm": 20.0,
            "Pressure9am": 1020.0,
            "Pressure3pm": 1018.0,
            "Cloud9am": 1.0,
            "Cloud3pm": 2.0,
            "Temp9am": 15.0,
            "Temp3pm": 26.0,
            "Evaporation": 4.0,
            "Sunshine": 9.0,
            "RainToday": 0,
        }
        result = trained_predictor.predict(input_data, model_choice="random_forest")

        assert result["prediction"] == 0
        assert result["label"] == "No"
        assert 0 <= result["confidence"] <= 100

    def test_rainy_day(self, trained_predictor):
        """High humidity, low pressure, rain today should predict rain tomorrow"""

        input_data = {
            "MinTemp": 15.0,
            "MaxTemp": 20.0,
            "Rainfall": 10.0,
            "WindGustSpeed": 55.0,
            "WindSpeed9am": 25.0,
            "WindSpeed3pm": 30.0,
            "Humidity9am": 95.0,
            "Humidity3pm": 98.0,
            "Pressure9am": 1000.0,
            "Pressure3pm": 998.0,
            "Cloud9am": 8.0,
            "Cloud3pm": 8.0,
            "Temp9am": 16.0,
            "Temp3pm": 18.0,
            "Evaporation": 2.0,
            "Sunshine": 1.0,
            "RainToday": 1
        }
        result = trained_predictor.predict(input_data, model_choice="random_forest")

        assert result["prediction"] == 1
        assert result["label"] == "Yes"
        assert 0 <= result["confidence"] <= 100

    def test_missing_feature(self, trained_predictor):
        """Test that missing features raise an error"""
        input_data = {
            "MinTemp": 15.0,
            # "MaxTemp" is missing
            "Rainfall": 10.0,
            "WindGustSpeed": 55.0,
            "WindSpeed9am": 25.0,
            "WindSpeed3pm": 30.0,
            "Humidity9am": 95.0,
            "Humidity3pm": 98.0,
            "Pressure9am": 1000.0,
            "Pressure3pm": 998.0,
            "Cloud9am": 8.0,
            "Cloud3pm": 8.0,
            "Temp9am": 16.0,
            "Temp3pm": 18.0,
            "RainToday": 1
        }
        with pytest.raises(ValueError):
            trained_predictor.predict(input_data, model_choice="random_forest")

    def test_before_training(self, weather_df):
        """Test that trying to predict before training raises an error"""
        predictor = RainPredictor(weather_df)
        input_data = {
            "MinTemp": 15.0,
            "MaxTemp": 20.0,
            "Rainfall": 10.0,
            "WindGustSpeed": 55.0,
            "WindSpeed9am": 25.0,
            "WindSpeed3pm": 30.0,
            "Humidity9am": 95.0,
            "Humidity3pm": 98.0,
            "Pressure9am": 1000.0,
            "Pressure3pm": 998.0,
            "Cloud9am": 8.0,
            "Cloud3pm": 8.0,
            "Temp9am": 16.0,
            "Temp3pm": 18.0,
            "RainToday": 1
        }
        with pytest.raises(ValueError):
            predictor.predict(input_data, model_choice="random_forest")