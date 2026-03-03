import logging
import asyncio
import pandas as pd
import csv
from importlib import resources

logger = logging.getLogger(__name__)


class DataLoader:
    """Retrieves data from csv files"""

    def __init__(self, files: list[str]):
        self.files = files
        self.package = "practice_data_sets.data"


    def _row_generator(self, filename: str):
        """
        Generator that yields rows from the csv file one at a time.
        This can be useful for processing large files without loading the entire dataset into memory.

        Args:
            filename (str): The name of the csv file to read from.
        """

        try:
            source = resources.files(self.package) / filename  # Join path
            with source.open(mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for line in reader:
                    yield line
        except FileNotFoundError:
            msg = f"File - {filename} - was not found."
            logger.error(msg)
            raise FileNotFoundError(msg)
        except Exception as e:
            msg = f"An error occurred while reading the file: {e}"
            logger.error(msg)
            raise Exception(msg)


    def _load_data(self, filename: str) -> pd.DataFrame:
        """
        Uses the row generator to load the data as needed into a pandas DataFrame.

        Args:
            filename (str): The name of the csv file to read from.

        Returns:
            pd.DataFrame: DataFrame containing the weather data.
        """

        logger.info(f"Streaming weather data from {filename} using the row generator")

        generator = self._row_generator(filename)
        header = [col.strip().strip('"') for col in next(generator)]  # Get the header row and strip quotes
        df = pd.DataFrame.from_records(generator, columns=header)  # Create DataFrame from the generator

        numeric_cols = ["MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine", "WindGustSpeed",
                        "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm", "Pressure9am",
                        "Pressure3pm", "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm"]

        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce') # Convert to numeric, coercing errors to NaN

        bool_cols = ["RainToday", "RainTomorrow"]
        for col in bool_cols:
            df[col] = df[col].map({'Yes': True, 'No': False,
                                   'yes': True, 'no': False,
                                   1: True, 0: False,
                                   1.0: True, 0.0: False,
                                   '1': True, '0': False})  # Convert values to True/False, handling various representations
        df[bool_cols] = df[bool_cols].astype('boolean')

        return df


    async def _async_loader(self, filename: str) -> pd.DataFrame:
        """
        Asynchronously loads the data from the csv file into a pandas DataFrame.

        Args:
            filename (str): The name of the csv file to read from.

        Returns:
            pd.DataFrame: DataFrame containing the weather data.
        """
        logger.info(f"Asynchronously loading weather data from {filename}")
        df = await asyncio.to_thread(self._load_data, filename)  # Run the synchronous load_data method in a separate thread
        return df


    async def load_files(self):
        """
        Asynchronously loads multiple files concurrently.

        Args:
            None

        Returns:
            pd.DataFrame: A list of DataFrames containing the weather data from each file.
        """
        tasks = [asyncio.create_task(self._async_loader(file)) for file in self.files]
        dataframes = await asyncio.gather(*tasks)
        combined_df = pd.concat(dataframes, ignore_index=True)  # Combine all DataFrames into one

        logger.info("All files successfully loaded and combined into a single DataFrame.")
        return combined_df

