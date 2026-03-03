import pytest
import asyncio
from practice_data_sets.visualize import DataVisualizer
from practice_data_sets.loader import DataLoader

@pytest.mark.asyncio
async def test_single_location_for_lists(tmp_path):
    # Load the data
    loader = DataLoader(["Weather Training Data.csv"])
    df = await loader.load_files()

    # Create an instance of DataVisualizer
    visualizer = DataVisualizer(df, output_dir=tmp_path)

    # Test with a single location in the list
    single_location = ["Albury"]
    visualizer.display_distribution_for_location(single_location, "temperature")
    visualizer.display_distribution_for_location(single_location, "rainfall")

@pytest.mark.asyncio
async def test_missing_location_for_lists(tmp_path):
    # Load the data
    loader = DataLoader(["Weather Training Data.csv"])
    df = await loader.load_files()

    # Create an instance of DataVisualizer
    visualizer = DataVisualizer(df, output_dir=tmp_path)

    # Test with a location that does not exist in the dataset
    missing_location = ["The Moon"]
    visualizer.display_distribution_for_location(missing_location, "temperature")
    visualizer.display_distribution_for_location(missing_location, "rainfall")

@pytest.mark.asyncio
async def test_multiple_locations_for_lists(tmp_path):
    # Load the data
    loader = DataLoader(["Weather Training Data.csv"])
    df = await loader.load_files()

    # Create an instance of DataVisualizer
    visualizer = DataVisualizer(df, output_dir=tmp_path)

    # Test with multiple locations in the list
    multiple_locations = ["Albury", "Sydney", "Melbourne"]
    visualizer.display_distribution_for_location(multiple_locations, "temperature")
    visualizer.display_distribution_for_location(multiple_locations, "rainfall")

@pytest.mark.asyncio
async def test_no_exceptions_all(tmp_path):
    # Load the data
    loader = DataLoader(["Weather Training Data.csv"])
    df = await loader.load_files()

    # Create an instance of DataVisualizer
    visualizer = DataVisualizer(df, output_dir=tmp_path)

    # Test that no exceptions are raised when calling all visualization methods

    visualizer.display_average_max_temperature_by_location()
    visualizer.display_distribution_for_location(["Albury", "Sydney"], "temperature")
    visualizer.display_distribution_for_location(["Albury", "Sydney"], "location")