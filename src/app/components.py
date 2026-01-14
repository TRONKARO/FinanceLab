import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from ..domain.models import AnalysisResult

def render_metric_card(label: str, value: str, delta: str = None, help_text: str = None):
    st.metric(label=label, value=value, delta=delta, help=help_text)

def plot_price_and_signals(ticker: str, df: pd.DataFrame, metrics):
    """
    Create a Plotly chart with Candlesticks and indicators.
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, row_heights=[0.7, 0.3])

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        name='Price'
    ), row=1, col=1)

    # SMAs
    # We need to re-calculate rolling for plotting since we only have last scalar in metrics
    # Or efficient way: pass the indicator series.
    # For now, let's recalculate quickly for plotting to keep signature simple, 
    # or better, the AnalysisResult could carry series data? 
    # To keep payload small, we'll calc here.
    sma50 = df['Close'].rolling(window=50).mean()
    sma200 = df['Close'].rolling(window=200).mean()

    fig.add_trace(go.Scatter(x=df.index, y=sma50, line=dict(color='orange', width=1), name='SMA 50'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=sma200, line=dict(color='blue', width=1), name='SMA 200'), row=1, col=1)

    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    fig.add_trace(go.Scatter(x=df.index, y=rsi, line=dict(color='purple', width=1), name='RSI'), row=2, col=1)
    
    # RSI Zones
    fig.add_hrect(y0=70, y1=100, row=2, col=1, fillcolor="red", opacity=0.1, line_width=0)
    fig.add_hrect(y0=0, y1=30, row=2, col=1, fillcolor="green", opacity=0.1, line_width=0)
    fig.add_hline(y=70, line_dash="dash", row=2, col=1, line_color="red")
    fig.add_hline(y=30, line_dash="dash", row=2, col=1, line_color="green")

    fig.update_layout(
        title=f"{ticker} Analysis",
        xaxis_rangeslider_visible=False,
        height=600,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_comparison_chart(data_dict: dict):
    """
    Plot normalized returns for comparison.
    """
    fig = go.Figure()
    
    for ticker, df in data_dict.items():
        if df.empty: continue
        # Normalize to start at 0%
        start_price = df['Close'].iloc[0]
        normalized = (df['Close'] - start_price) / start_price
        
        fig.add_trace(go.Scatter(x=df.index, y=normalized, mode='lines', name=ticker))
        
    fig.update_layout(
        title="Relative Performance Comparison",
        yaxis_title="Return (%)",
        yaxis_tickformat='.1%',
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
