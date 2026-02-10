"""An application entry point"""
import logging
from practice_data_sets.loader import DataLoader
from practice_data_sets.stats import DataProcessor


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def main():
    """
    Entry point for the script.
    """

    # Load the weather data
    # loader = DataLoader("Weather Training Data.csv")
    loader = DataLoader("Missing File Test.csv")   # Intentionally using a missing file to demonstrate error handling
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
