import sqlite3
import pandas as pd
import io
import os
from datetime import datetime, timedelta
from typing import Optional

class DataCache:
    def __init__(self, db_path: str = "finance_lab_cache.db", ttl_hours: int = 6):
        """
        Initialize SQLite cache for storing stock data.
        
        Args:
            db_path: Path to the sqlite database file
            ttl_hours: Time to live for cached data in hours
        """
        self.db_path = db_path
        self.ttl_hours = ttl_hours
        self._init_db()

    def _init_db(self):
        """Create tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_data (
                ticker TEXT,
                period TEXT,
                updated_at TIMESTAMP,
                data BLOB,
                PRIMARY KEY (ticker, period)
            )
        """)
        conn.commit()
        conn.close()

    def get_data(self, ticker: str, period: str) -> Optional[pd.DataFrame]:
        """
        Retrieve data from cache if it exists and hasn't expired.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT updated_at, data FROM stock_data WHERE ticker = ? AND period = ?", 
            (ticker, period)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            updated_at_str, blob = row
            updated_at = datetime.fromisoformat(updated_at_str)
            
            # Check TTL
            if datetime.now() - updated_at < timedelta(hours=self.ttl_hours):
                try:
                    # Read parquet from bytes
                    return pd.read_parquet(io.BytesIO(blob))
                except Exception as e:
                    print(f"Error reading cache for {ticker}: {e}")
                    return None
            else:
                # Expired
                return None
        return None

    def save_data(self, ticker: str, period: str, df: pd.DataFrame):
        """
        Save dataframe to cache.
        """
        try:
            # Convert DF to parquet bytes
            buffer = io.BytesIO()
            df.to_parquet(buffer, compression='snappy')
            blob = buffer.getvalue()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            updated_at = datetime.now().isoformat()
            
            cursor.execute(
                """
                INSERT OR REPLACE INTO stock_data (ticker, period, updated_at, data)
                VALUES (?, ?, ?, ?)
                """,
                (ticker, period, updated_at, blob)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving to cache for {ticker}: {e}")
