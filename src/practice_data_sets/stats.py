import pandas as pd
from pandas import DataFrame


class DataProcessor:
    """Processes weather data"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def describe_weather_data(self) -> dict[str, DataFrame]:
        """
        Displays weather information from the DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing the weather data.

        Returns: -
            Head and description of the DataFrame.
        """

        return {
            "head": self.df.head(),
            "description": self.df.describe()
        }


