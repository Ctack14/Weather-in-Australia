import logging
import pandas as pd
from importlib.resources import open_text



logger = logging.getLogger(__name__)


class DataLoader:
    """Retrieves data from csv files"""

    def __init__(self, filename: str):
        self.filename = filename

    def row_generator(self):
        """
        Generator that yields rows from the csv file one at a time.
        This can be useful for processing large files without loading the entire dataset into memory.

        Args:
            None
        """

        try:
            with open_text("practice_data_sets.data", self.filename) as data_path:
                for line in data_path:
                    yield line.strip().split(",")
        except FileNotFoundError:
            logger.error(f"File {self.filename} not found.")
            raise
        except Exception as e:
            logger.error(f"An error occurred while reading the file: {e}")
            raise


    def load_data(self) -> pd.DataFrame:
        """
        Uses the row generator to load the data as needed into a pandas DataFrame.

        Args:
            None

        Returns:
            pd.DataFrame: DataFrame containing the weather data.
        """

        logger.info("Loading weather data")

        data = list(self.row_generator())
        return pd.DataFrame(data)

