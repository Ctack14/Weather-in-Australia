import asyncio
import pytest
import pandas as pd
from src.practice_data_sets.loader import DataLoader
import asyncio

def test_row_generator():
    """Tests that the row generator yields rows correctly."""
    loader = DataLoader(["Weather Training Data.csv"])
    rows = list(loader._row_generator("Weather Training Data.csv"))

    assert len(rows) > 0
    assert isinstance(rows[0], list)

@pytest.mark.asyncio
async def test_load_data():
    """Tests that the load_data method returns a DataFrame."""
    loader = DataLoader(["Weather Training Data.csv"])
    df = await loader.load_files()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    loader2 = DataLoader(["Weather Training Data.csv", "a_test_file.csv"])
    df2 = await loader2.load_files()
    assert isinstance(df2, pd.DataFrame)
    assert not df2.empty

@pytest.mark.asyncio
async def test_file_not_found():
    """Tests that a FileNotFoundError is raised when the file is missing."""
    loader = DataLoader(["Missing File Test.csv"])
    with pytest.raises(FileNotFoundError, match="File - Missing File Test.csv - was not found."):
        df = await loader.load_files()

    loader2 = DataLoader(["Weather Training Data.csv", "Missing File Test.csv"])
    with pytest.raises(FileNotFoundError, match="File - Missing File Test.csv - was not found."):
        df = await loader2.load_files()
