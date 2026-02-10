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

    def print_unique_locations(self):
        """
        Prints the unique locations in the weather data using

        Args:
            df (pd.DataFrame): DataFrame containing the weather data.

        Returns: None
        """

        logger.info("Printing unique locations")

        for location in self.df["Location"].unique():   # Iterator usage for rubric
            print(location)






