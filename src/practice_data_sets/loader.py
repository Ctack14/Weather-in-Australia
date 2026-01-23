import pandas as pd
from importlib.resources import files

def load_weather_data() -> pd.DataFrame:
    """
    Loads weather data from a csv file into a pandas DataFrame.

    Args:
        None

    Returns:
        pd.DataFrame: DataFrame containing the weather data.
    """
    data_path = files("practice_data_sets.data") / "Weather Training Data.csv"
    return pd.read_csv(data_path)
