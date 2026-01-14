from dataclasses import dataclass
from typing import Optional, List, Dict
import pandas as pd

@dataclass
class AssetMetrics:
    current_price: float
    daily_return: float
    total_return: float
    volatility: float
    max_drawdown: float
    rsi: float
    sma_20: float
    sma_50: float
    sma_200: float

@dataclass
class AnalysisResult:
    ticker: str
    metrics: AssetMetrics
    score: float
    recommendation: str  # "Buy", "Hold", "Sell"
    reasoning: List[str]
    risk_profile: str

@dataclass
class Watchlist:
    name: str
    tickers: List[str]
