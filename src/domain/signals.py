from typing import List, Dict
import pandas as pd
import numpy as np
from .models import AnalysisResult, AssetMetrics
from ..analysis.indicators import calculate_rsi, calculate_sma
from ..analysis.metrics import (
    calculate_daily_returns, calculate_cumulative_return, 
    calculate_volatility, calculate_max_drawdown
)

class SignalEngine:
    RISK_PROFILES = {
        "Conservative": {"risk_penalty": 2.0, "momentum_weight": 0.5, "trend_weight": 1.0},
        "Moderate": {"risk_penalty": 1.0, "momentum_weight": 1.0, "trend_weight": 1.0},
        "Aggressive": {"risk_penalty": 0.5, "momentum_weight": 1.5, "trend_weight": 1.2},
    }

    def analyze_ticker(self, ticker: str, df: pd.DataFrame, risk_profile: str) -> AnalysisResult:
        if df.empty or len(df) < 50:
            # Not enough data
            return self._empty_result(ticker, risk_profile)

        # 1. Calculate Indicators
        prices = df['Close']
        rsi = calculate_rsi(prices, 14)
        sma20 = calculate_sma(prices, 20)
        sma50 = calculate_sma(prices, 50)
        sma200 = calculate_sma(prices, 200)
        
        # 2. Calculate Metrics
        daily_rets = calculate_daily_returns(prices)
        vol = calculate_volatility(daily_rets)
        mdd = calculate_max_drawdown(prices)
        total_ret = calculate_cumulative_return(prices)
        
        current_price = prices.iloc[-1]
        current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50.0
        
        metrics = AssetMetrics(
            current_price=current_price,
            daily_return=daily_rets.iloc[-1] if len(daily_rets) > 0 else 0.0,
            total_return=total_ret,
            volatility=vol,
            max_drawdown=mdd,
            rsi=current_rsi,
            sma_20=sma20.iloc[-1] if not pd.isna(sma20.iloc[-1]) else 0.0,
            sma_50=sma50.iloc[-1] if not pd.isna(sma50.iloc[-1]) else 0.0,
            sma_200=sma200.iloc[-1] if not pd.isna(sma200.iloc[-1]) else 0.0,
        )

        # 3. Generate Signals
        rec, reasoning = self._generate_recommendation(prices, rsi, sma50, sma200)
        
        # 4. Calculate Score
        score = self._calculate_score(metrics, risk_profile)

        return AnalysisResult(
            ticker=ticker,
            metrics=metrics,
            score=score,
            recommendation=rec,
            reasoning=reasoning,
            risk_profile=risk_profile
        )

    def _generate_recommendation(self, prices, rsi, sma50, sma200):
        signals = []
        score = 0
        
        curr_price = prices.iloc[-1]
        curr_rsi = rsi.iloc[-1]
        curr_sma50 = sma50.iloc[-1]
        curr_sma200 = sma200.iloc[-1]

        # Trend Signals
        if curr_sma50 > curr_sma200:
            signals.append("Golden Cross (Bullish Trend)")
            score += 1
        elif curr_sma50 < curr_sma200:
            signals.append("Death Cross (Bearish Trend)")
            score -= 1
            
        if curr_price > curr_sma200:
            signals.append("Price above SMA 200 (Long-term Bullish)")
            score += 1
        else:
            signals.append("Price below SMA 200 (Long-term Bearish)")
            score -= 1
            
        # Momentum Signals
        if curr_rsi < 30:
            signals.append(f"RSI Oversold ({curr_rsi:.1f}) -> Potential Buy")
            score += 2
        elif curr_rsi > 70:
            signals.append(f"RSI Overbought ({curr_rsi:.1f}) -> Potential Sell")
            score -= 2
        else:
            signals.append(f"RSI Neutral ({curr_rsi:.1f})")

        # Decision
        if score >= 2:
            rec = "Buy"
        elif score <= -2:
            rec = "Sell"
        else:
            rec = "Hold"
            
        return rec, signals

    def _calculate_score(self, metrics: AssetMetrics, risk_profile: str) -> float:
        """
        Score from 0 to 100.
        """
        weights = self.RISK_PROFILES.get(risk_profile, self.RISK_PROFILES["Moderate"])
        
        # Normalize metrics (approximate logic for demonstration)
        # Trend Score (0-100)
        trend_score = 50
        if metrics.current_price > metrics.sma_200: trend_score += 25
        if metrics.sma_50 > metrics.sma_200: trend_score += 25
        
        # Risk Score (Higher volatility/Drawdown -> Lower Score)
        # Volatility: low < 15%, high > 40%
        # MDD: low > -10%, high < -30%
        
        vol_penalty = min(metrics.volatility * 100, 50) * weights["risk_penalty"]
        mdd_penalty = min(abs(metrics.max_drawdown) * 100, 50) * weights["risk_penalty"]
        
        risk_adj = 100 - (vol_penalty + mdd_penalty)
        risk_score = max(0, risk_adj)
        
        # Momentum Score
        # RSI 30-70 is neutral. <30 is opportunity (high score), >70 is risk (low score) - usually inverted for scoring?
        # Actually for a "rating", usually Up Trend = High Score.
        # But RSI Oversold (30) is buy signal. So let's align Score with "Good to Buy".
        momentum_score = 50
        if metrics.rsi < 30: momentum_score = 90
        elif metrics.rsi > 70: momentum_score = 20
        else: momentum_score = 50 + (50 - metrics.rsi) # e.g. 50 -> 50, 40 -> 60, 60 -> 40
        
        # Composite
        final_score = (
            (trend_score * weights["trend_weight"]) + 
            (risk_score * weights["momentum_weight"]) # Using momentum_weight just as a 2nd weight
             + (momentum_score * weights["momentum_weight"])
        ) / (weights["trend_weight"] + weights["momentum_weight"]*2)
        
        return min(max(final_score, 0), 100)

    def _empty_result(self, ticker, risk_profile):
        m = AssetMetrics(
            current_price=0, daily_return=0, total_return=0, volatility=0, 
            max_drawdown=0, rsi=0, sma_20=0, sma_50=0, sma_200=0
        )
        return AnalysisResult(ticker, m, 0, "N/A", ["Insufficient Data"], risk_profile)
