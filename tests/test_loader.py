import pytest
import pandas as pd
from src.practice_data_sets.loader import DataLoader

def test_row_generator():
    """Tests that the row generator yields rows correctly."""
    loader = DataLoader("Weather Training Data.csv")
    rows = list(loader.row_generator())

    assert len(rows) > 0
    assert isinstance(rows[0], list)


def test_load_data():
    """Tests that the load_data method returns a DataFrame."""
    loader = DataLoader("Weather Training Data.csv")
    df = loader.load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_file_not_found():
    """Tests that a FileNotFoundError is raised when the file is missing."""
    loader = DataLoader("Missing File Test.csv")
    with pytest.raises(FileNotFoundError, match="File | Missing File Test.csv | was not found."):
        loader.load_data()
