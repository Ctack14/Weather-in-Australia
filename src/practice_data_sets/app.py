"""An application entry point"""
import logging
from practice_data_sets.loader import DataLoader
from practice_data_sets.stats import DataProcessor
from visualize import DataVisualizer
import asyncio



logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

async def main():
    """
    Entry point for the script.
    """

    # Load the weather data
    loader = DataLoader(["Weather Training Data.csv"])

    weather_df = await loader.load_files()

    # Process and describe the weather data
    processor = DataProcessor(weather_df)
    results = processor.describe_weather_data()

    # Visualize the weather data
    locations = weather_df["Location"].unique()
    visualizer = DataVisualizer(weather_df)

    visualizer.display_distribution_for_location(locations, "temperature")
    visualizer.display_distribution_for_location(locations, "rainfall")

    # Display the results
    print("Weather Data Overview:")
    print(results["head"])
    print("\nData Summary:")
    print(results["description"])



if __name__ == "__main__":
    asyncio.run(main())
