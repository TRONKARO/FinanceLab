import pytest
import pandas as pd
import os
import shutil
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.data.storage import DataCache
from src.data.loader import DataLoader

# Test fixture for temporary cache db
@pytest.fixture
def temp_cache():
    db_name = "test_cache.db"
    cache = DataCache(db_path=db_name, ttl_hours=1)
    yield cache
    # Cleanup
    if os.path.exists(db_name):
        os.remove(db_name)

def test_cache_save_and_get(temp_cache):
    df = pd.DataFrame({"Close": [100, 101, 102]}, index=[1, 2, 3])
    ticker = "TEST"
    period = "1mo"
    
    # Save
    temp_cache.save_data(ticker, period, df)
    
    # Get
    retrieved_df = temp_cache.get_data(ticker, period)
    assert retrieved_df is not None
    assert retrieved_df.equals(df)

def test_cache_ttl_expiry():
    db_name = "test_ttl.db"
    cache = DataCache(db_path=db_name, ttl_hours=-1) # Immediate expiry
    
    df = pd.DataFrame({"Close": [10]})
    cache.save_data("TEST", "1d", df)
    
    # Should be expired
    assert cache.get_data("TEST", "1d") is None
    
    if os.path.exists(db_name):
        os.remove(db_name)

@patch("src.data.loader.yf.download")
def test_loader_fetch_and_cache(mock_download):
    # Setup mock
    mock_df = pd.DataFrame({"Close": [150.0]}, index=pd.Index([datetime.now()], name="Date"))
    mock_download.return_value = mock_df
    
    loader = DataLoader()
    # Use a test db for loader
    loader.cache = DataCache(db_path="loader_test.db")
    
    # 1. Fetch (should call yfinance)
    df = loader.get_ticker_history("AAPL", "1mo")
    assert df is not None
    assert not df.empty
    mock_download.assert_called_once()
    
    # 2. Fetch again (should hit cache, not yfinance)
    mock_download.reset_mock()
    df_cached = loader.get_ticker_history("AAPL", "1mo")
    assert df_cached is not None
    mock_download.assert_not_called()
    
    # Cleanup
    if os.path.exists("loader_test.db"):
        os.remove("loader_test.db")

