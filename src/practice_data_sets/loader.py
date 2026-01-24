import pandas as pd
from importlib.resources import open_text

def load_weather_data() -> pd.DataFrame:
    """
    Loads weather data from a csv file into a pandas DataFrame.
    Uses importlib.resources to access the data file, which will work both in development and when packaged
    across different environments.

    Args:
        None

    Returns:
        pd.DataFrame: DataFrame containing the weather data.
    """
    with open_text("practice_data_sets.data", "Weather Training Data.csv") as data_path:
        return pd.read_csv(data_path)
