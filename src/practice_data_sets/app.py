"""An application entry point"""

from practice_data_sets.loader import DataLoader
from practice_data_sets.stats import DataProcessor


def main():
    """
    Entry point for the script.
    """

    # Load the weather data
    loader = DataLoader("Weather Training Data.csv")
    weather_df = loader.load_data()

    # Process and describe the weather data
    processor = DataProcessor(weather_df)
    results = processor.describe_weather_data()

    # Display the results
    print("Weather Data Overview:")
    print(results["head"])
    print("\nData Summary:")
    print(results["description"])



if __name__ == "__main__":
    main()
