import pandas as pd
import numpy as np

def calculate_daily_returns(series: pd.Series) -> pd.Series:
    return series.pct_change()

def calculate_cumulative_return(series: pd.Series) -> float:
    if len(series) < 1:
        return 0.0
    start = series.iloc[0]
    end = series.iloc[-1]
    if start == 0: return 0.0
    return (end - start) / start

def calculate_volatility(daily_returns: pd.Series, annualized: bool = True) -> float:
    """Annualized volatility."""
    vol = daily_returns.std()
    if annualized:
        vol = vol * np.sqrt(252) # 252 trading days
    return vol

def calculate_max_drawdown(series: pd.Series) -> float:
    """Calculate Maximum Drawdown from peak."""
    rolling_max = series.cummax()
    drawdown = (series - rolling_max) / rolling_max
    return drawdown.min()
