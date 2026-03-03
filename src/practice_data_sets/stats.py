import logging
import pandas as pd
from pandas import DataFrame

logger = logging.getLogger(__name__)

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

        logger.info("Describing weather data")

        return {
            "head": self.df.head(),
            "description": self.df.describe()
        }

    def find_unique_locations(self):
        """
        Finds and returns a list of unique locations from the DataFrame.

        Args:
            None

        Returns: A list of unique locations in the DataFrame.
        """

        logger.info("Printing unique locations")

        return list(self.df["Location"].unique())


