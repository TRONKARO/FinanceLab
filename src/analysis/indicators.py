import pandas as pd
import numpy as np

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Fill NaN with 50 (neutral) or maintain NaN depending on preference.
    # Usually better to leave NaN for early values.
    return rsi

def calculate_sma(series: pd.Series, window: int) -> pd.Series:
    """Calculate Simple Moving Average."""
    return series.rolling(window=window).mean()

def calculate_bollinger_bands(series: pd.Series, window: int = 20, num_std: int = 2):
    """Calculate Bollinger Bands (Upper, Middle, Lower)."""
    sma = calculate_sma(series, window)
    std = series.rolling(window=window).std()
    upper = sma + (std * num_std)
    lower = sma - (std * num_std)
    return upper, sma, lower
