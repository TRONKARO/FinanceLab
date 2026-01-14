import pytest
import pandas as pd
import numpy as np
from src.analysis.indicators import calculate_rsi, calculate_sma
from src.analysis.metrics import calculate_daily_returns, calculate_max_drawdown
from src.domain.signals import SignalEngine

def test_rsi_calculation():
    # Simple pattern to test RSI
    prices = pd.Series([100, 102, 104, 106, 108, 100, 95, 90, 85, 80, 82, 84, 86, 88, 90, 92])
    rsi = calculate_rsi(prices, period=5)
    # RSI should be valid eventually
    assert not pd.isna(rsi.iloc[-1])
    # Last value should be > 50 because it's rising
    assert rsi.iloc[-1] > 50

def test_sma_calculation():
    prices = pd.Series([1, 2, 3, 4, 5])
    sma = calculate_sma(prices, window=3)
    assert pd.isna(sma.iloc[1])
    assert sma.iloc[2] == 2.0  # (1+2+3)/3

def test_metrics():
    # Volatility
    prices = pd.Series([100, 101, 100, 101])
    rets = calculate_daily_returns(prices)
    assert len(rets) == 4
    
    # MDD
    prices_mdd = pd.Series([100, 120, 90, 110]) # Peak 120, Low 90. Drop 30. 30/120 = 25%
    mdd = calculate_max_drawdown(prices_mdd)
    assert mdd == -0.25

def test_signal_engine_scoring():
    engine = SignalEngine()
    
    # Mock DF with clear upward trend
    dates = pd.date_range("2023-01-01", periods=200)
    prices = [100 + i for i in range(200)] # Constant rise
    df = pd.DataFrame({"Close": prices}, index=dates)
    
    result = engine.analyze_ticker("TEST", df, "Moderate")
    
    assert result.ticker == "TEST"
    assert result.score > 50 # Application of positive trend
    assert result.recommendation in ["Buy", "Hold"] # Should likely be Buy or Hold
