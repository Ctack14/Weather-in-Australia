import pandas as pd
from importlib.resources import open_text


class DataLoader:
    """Retrieves data from csv files"""

    def __init__(self, filename: str):
        self.filename = filename


    def load_data(self) -> pd.DataFrame:
        """
        Loads weather data from a csv file into a pandas DataFrame.
        Uses importlib.resources to access the data file, which will work both in development and when packaged
        across different environments.

        Args:
            None

        Returns:
            pd.DataFrame: DataFrame containing the weather data.
        """
        with open_text("practice_data_sets.data", self.filename) as data_path:
            return pd.read_csv(data_path)
