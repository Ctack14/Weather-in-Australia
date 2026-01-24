import pandas as pd

def describe_weather_data(df: pd.DataFrame) -> None:
    """
    Displays weather information from the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the weather data.

    Returns: -
        None
    """
    print("Weather Data Overview:")
    print(df.head())
    print("\nData Summary:")
    print(df.describe())