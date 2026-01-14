import yfinance as yf
import pandas as pd
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from .storage import DataCache

load_dotenv()

class DataLoader:
    def __init__(self):
        # Allow overriding cache settings via env vars
        ttl = int(os.getenv("CACHE_TTL_HOURS", "6"))
        self.cache = DataCache(ttl_hours=ttl)

    def get_ticker_history(self, ticker: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Fetch historical data for a single ticker. Checks cache first.
        
        Args:
            ticker: Symbol (e.g. AAPL, SPY)
            period: valid yfinance period (1m, 3m, 6m, 1y, 5y, max)
        
        Returns:
            pd.DataFrame with OHLCV data or None if failed
        """
        # Try cache first
        cached_df = self.cache.get_data(ticker, period)
        if cached_df is not None:
            return cached_df

        # Fetch from API
        try:
            # yfinance download
            df = yf.download(ticker, period=period, progress=False, multi_level_index=False)
            
            if df is None or df.empty:
                return None
            
            # Reset index to make Date a column if it's the index, useful for some operations
            # But standard is usually Date index. Let's keep Date as index but ensure it's datetime.
            # yfinance returns Date index.
            
            # Simple validation
            if 'Close' not in df.columns:
                return None
                
            # Save to cache
            self.cache.save_data(ticker, period, df)
            return df
            
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None

    def get_batch_history(self, tickers: List[str], period: str = "1y") -> Dict[str, pd.DataFrame]:
        """
        Fetch history for multiple tickers.
        """
        results = {}
        for t in tickers:
            data = self.get_ticker_history(t, period)
            if data is not None:
                results[t] = data
        return results
