"""Read Australian weather data from a CSV file and display basic information."""

import pandas as pd

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Loads weather data from a csv file into a pandas DataFrame.

    Args:
        CSV path (str): the path to the csv file.

    Returns:
        pd.DataFrame: DataFrame containing the weather data.
    """
    return pd.read_csv(file_path)

def display_weather_info(df: pd.DataFrame) -> None:
    """
    Displays weather information from the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the weather data.

    Returns:
        None
    """
    print("Weather Data Overview:")
    print(df.head())
    print("\nData Summary:")
    print(df.describe())

def main():
    """
    Entry point for the script.
    """

    file_path = "Weather Training Data.csv"
    weather_df = load_csv(file_path)
    display_weather_info(weather_df)


if __name__ == "__main__":
    main()
