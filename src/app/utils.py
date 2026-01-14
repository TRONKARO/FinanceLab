import pandas as pd
from datetime import datetime, timedelta

def get_valid_periods():
    return ["1mo", "3mo", "6mo", "1y", "2y", "5y", "ytd"]

def get_risk_profiles():
    return ["Conservative", "Moderate", "Aggressive"]

def format_percentage(value: float) -> str:
    return f"{value*100:.2f}%"

def format_currency(value: float) -> str:
    return f"${value:.2f}"

def get_default_tickers():
    return [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", 
        "SPY", "QQQ", "GLD", "KO", "JNJ",
        "NVDA", "AMD", "WMT", "DIS", "V"
    ]
