import streamlit as st
import pandas as pd
from typing import List

import sys
import os

# Add the project root to the python path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.app.utils import get_valid_periods, get_risk_profiles, get_default_tickers, format_percentage, format_currency
from src.app.components import render_metric_card, plot_price_and_signals, render_comparison_chart
from src.app.translations import get_text
from src.data.loader import DataLoader
from src.domain.signals import SignalEngine
from src.domain.models import AnalysisResult

# Page Config
st.set_page_config(
    page_title="FinanceLab",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    .stMetric {
        background-color: white; 
        padding: 10px; 
        border-radius: 5px; 
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # --- Sidebar ---
    with st.sidebar:
        st.header(get_text("en", "config_header")) # Default header initially, will update
        
        # Language Selector
        lang_code = st.selectbox("Language / Idioma", ["en", "es"], format_func=lambda x: "English" if x == "en" else "Español")
        
        # Helper to get text with current lang
        def t(key):
            return get_text(lang_code, key)
            
        st.markdown("---")
        
        # Risk Profile
        risk_profile = st.selectbox(
            t("risk_profile"), 
            get_risk_profiles(),
            index=1,
            help=t("risk_profile_help")
        )
        
        # Period
        period = st.selectbox(t("analysis_period"), get_valid_periods(), index=3) # Default 1y
        
        # Input Watchlist
        default_tickers_str = ", ".join(get_default_tickers())
        ticker_input = st.text_area(
            t("watchlist"), 
            value=default_tickers_str,
            height=150
        )
        
        analyze_btn = st.button(t("analyze_btn"), type="primary")
        
        with st.expander(t("about")):
            st.info(t("about_text"))
        
        st.markdown("---")
        with st.expander(t("disclaimer_title")):
            st.warning(t("disclaimer_text"))

    # --- Main Logic ---
    st.title(t("title"))
    st.markdown(t("description"))

    if analyze_btn or "results" not in st.session_state:
        if analyze_btn:
            with st.spinner(t("spinner")):
                loader = DataLoader() # Initialize data loader
                engine = SignalEngine() # Initialize signal engine
                
                tickers = [tik.strip().upper() for tik in ticker_input.split(",") if tik.strip()]
                
                results: List[AnalysisResult] = []
                comparison_data = {}
                
                progress_bar = st.progress(0)
                
                for i, ticker in enumerate(tickers):
                    df = loader.get_ticker_history(ticker, period)
                    if df is not None and not df.empty:
                        # Analyze
                        res = engine.analyze_ticker(ticker, df, risk_profile)
                        results.append(res)
                        comparison_data[ticker] = df
                    else:
                        st.warning(t("warning_fetch").format(ticker))
                    
                    progress_bar.progress((i + 1) / len(tickers))
                
                # Sort by score desc
                results.sort(key=lambda x: x.score, reverse=True)
                
                st.session_state["results"] = results
                st.session_state["comparison_data"] = comparison_data
                st.session_state["analyzed"] = True
                
    if st.session_state.get("analyzed"):
        results = st.session_state["results"]
        comparison_data = st.session_state["comparison_data"]
        
        # --- Tabs ---
        tab1, tab2, tab3 = st.tabs([t("tab_ranking"), t("tab_detail"), t("tab_comparison")])
        
        with tab1:
            st.subheader(t("ranking_subheader").format(len(results)))
            
            # Prepare DataFrame for display
            summary_data = []
            for r in results:
                summary_data.append({
                    t("col_ticker"): r.ticker,
                    t("metric_score"): f"{r.score:.1f}",
                    t("metric_recommendation"): r.recommendation,
                    t("col_price"): format_currency(r.metrics.current_price),
                    t("col_return"): format_percentage(r.metrics.total_return),
                    t("col_vol"): format_percentage(r.metrics.volatility),
                    t("col_rsi"): f"{r.metrics.rsi:.1f}",
                })
            
            st.dataframe(
                pd.DataFrame(summary_data).set_index(t("col_ticker")),
                use_container_width=True,
                height=500
            )
            
            # CSV Download
            csv = pd.DataFrame(summary_data).to_csv(index=False).encode('utf-8')
            st.download_button(
                t("download_csv"),
                csv,
                "financelab_report.csv",
                "text/csv",
                key='download-csv'
            )
 
        with tab2:
            st.subheader(t("deep_dive_subheader"))
            selected_ticker = st.selectbox(t("select_asset"), [r.ticker for r in results])
            
            # Find result
            res = next((r for r in results if r.ticker == selected_ticker), None)
            df = comparison_data.get(selected_ticker)
            
            if res and df is not None:
                # Top Metrics
                c1, c2, c3, c4 = st.columns(4)
                c1.metric(t("metric_score"), f"{res.score:.1f}/100", help=t("score_help"))
                c2.metric(t("metric_recommendation"), res.recommendation, delta=None) 
                c3.metric(t("col_rsi") + " (14)", f"{res.metrics.rsi:.1f}")
                c4.metric(t("metric_max_dd"), format_percentage(res.metrics.max_drawdown))
                
                # Chart
                plot_price_and_signals(selected_ticker, df, res.metrics)
                
                # Signals
                st.write(f"### {t('signals_header')}")
                if res.reasoning:
                    for reason in res.reasoning:
                        if "Buy" in reason or "Bullish" in reason:
                            st.success(reason)
                        elif "Sell" in reason or "Bearish" in reason:
                            st.error(reason)
                        else:
                            st.info(reason)
                else:
                    st.write(t("no_signals"))
 
        with tab3:
            st.subheader(t("comparison_subheader"))
            # Multi-select for comparison, default top 5
            top_5 = [r.ticker for r in results[:5]]
            compare_list = st.multiselect(t("select_compare"), [r.ticker for r in results], default=top_5)
            
            if compare_list:
                subset = {k: v for k, v in comparison_data.items() if k in compare_list}
                render_comparison_chart(subset)

        # Floating Chatbot using Popover
        with st.sidebar:
            st.markdown("---")
            
            # Custom CSS to make the popover button "flashy"
            st.markdown("""
            <style>
            /* Target all buttons in sidebar that are NOT the primary action button */
            [data-testid="stSidebar"] button:not([kind="primary"]),
            [data-testid="stSidebar"] button[kind="secondary"] {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: white !important;
                border: none !important;
                padding: 15px !important;
                font-size: 20px !important;
                font-weight: 800 !important;
                border-radius: 12px !important;
                box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4) !important;
                transition: all 0.3s ease !important;
                margin-top: 10px !important;
                text-align: center !important;
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                width: 100% !important;
            }
            
            /* Target internal text/paragraph to ensure font size inherits */
            [data-testid="stSidebar"] button:not([kind="primary"]) p,
            [data-testid="stSidebar"] button[kind="secondary"] p {
                font-size: 20px !important;
                font-weight: 800 !important;
                color: white !important;
            }

            /* Hover Effects */
            [data-testid="stSidebar"] button:not([kind="primary"]):hover,
            [data-testid="stSidebar"] button[kind="secondary"]:hover {
                transform: translateY(-2px) scale(1.02) !important;
                box-shadow: 0 8px 25px rgba(118, 75, 162, 0.6) !important;
                background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
                border: none !important;
                color: white !important;
            }

            /* Active State */
            [data-testid="stSidebar"] button:not([kind="primary"]):active,
            [data-testid="stSidebar"] button[kind="secondary"]:active  {
                transform: scale(0.98) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Popover for chat
            with st.popover(t("tab_assistant"), use_container_width=True, help=t("bot_welcome")):
                st.markdown(f"### {t('tab_assistant')}")
                
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                    # Initial greeting
                    st.session_state.messages.append({"role": "assistant", "content": t("bot_welcome")})

                # Display chat messages
                # Limit height to make it scrollable inside popover
                with st.container(height=300):
                    for message in st.session_state.messages:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])

                # Chat input
                if prompt := st.chat_input(t("bot_placeholder")):
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    # Generate response
                    response = ""
                    
                    # 1. Identify Ticker
                    found_ticker = None
                    for r in results:
                        if r.ticker in prompt.upper():
                            found_ticker = r
                            break
                    
                    if found_ticker:
                        # Select Template based on recommendation
                        rec_key = "bot_hold_recommendation" # Default
                        if "Buy" in found_ticker.recommendation:
                            rec_key = "bot_buy_recommendation"
                        elif "Sell" in found_ticker.recommendation:
                            rec_key = "bot_sell_recommendation"
                        
                        # Prepare long reasoning
                        signals_list = found_ticker.reasoning if found_ticker.reasoning else [t("no_signals")]
                        reasoning_long = "\n".join([f"- {s}" for s in signals_list])
                        
                        response = t(rec_key).format(
                            ticker=found_ticker.ticker,
                            score=f"{found_ticker.score:.1f}",
                            rsi=f"{found_ticker.metrics.rsi:.1f}",
                            vol=f"{found_ticker.metrics.volatility:.1%}",
                            reasoning=reasoning_long
                        )
                    else:
                        response = t("bot_unknown_ticker").format("...")
                        if "hola" in prompt.lower() or "hello" in prompt.lower():
                            response = t("bot_welcome")
                    
                    # Add assistant message
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    # Rerun to show new message
                    st.rerun()
    else:
        # Show message if no analysis has been run
         pass


if __name__ == "__main__":
    main()
