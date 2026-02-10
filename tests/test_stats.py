import pytest
import pandas as pd
from src.practice_data_sets.stats import DataProcessor


def sample_dataframe():
    """Creates a sample DataFrame for testing."""
    data = {
        "Location": ["CityA", "CityB", "CityC"],
        "Temperature": [20, 25, 30],
        "Humidity": [50, 60, 70]
    }
    return pd.DataFrame(data)


def test_describe_weather_data():
    """ Tests that the describe_weather_data method returns the correct head and description."""
    df = sample_dataframe()
    processor = DataProcessor(df)
    results = processor.describe_weather_data()

    assert "head" in results
    assert "description" in results
    assert isinstance(results["head"], pd.DataFrame)
    assert isinstance(results["description"], pd.DataFrame)
    assert not results["head"].empty
    assert not results["description"].empty

def test_print_unique_locations(capsys):
    """Tests the usage of an iterator to print unique locations."""
    df = sample_dataframe()
    processor = DataProcessor(df)
    processor.print_unique_locations()

    captured = capsys.readouterr()
    assert "CityA" in captured.out
    assert "CityB" in captured.out
    assert "CityC" in captured.out