TRANSLATIONS = {
    "en": {
        "title": "FinanceLab: Market Analyzer & CEDEAR Screener",
        "description": "Professional-grade technical analysis and risk scoring for portfolio management.",
        "config_header": "Configuration",
        "language": "Language",
        "risk_profile": "Risk Profile",
        "risk_profile_help": "Determines how the scoring engine weights volatility vs momentum.",
        "analysis_period": "Analysis Period",
        "watchlist": "Watchlist (comma separated)",
        "analyze_btn": "Analyze Market",
        "about": "About",
        "about_text": "Built with Python, Streamlit, yFinance & Plotly.",
        "disclaimer_title": "⚠️ Disclaimer",
        "disclaimer_text": "This application is for informational purposes only and does not constitute financial advice. Investment involves risk, including possible loss of principal. The creators of this application are not responsible for any financial losses.",
        "spinner": "Fetching data and calculating scores...",
        "warning_fetch": "Could not fetch data for {}",
        "tab_ranking": "📊 Summary Ranking",
        "tab_detail": "🔎 Ticker Detail",
        "tab_comparison": "📈 Comparison",
        "ranking_subheader": "Asset Ranking ({} assets)",
        "download_csv": "Download Report (CSV)",
        "deep_dive_subheader": "Deep Dive Analysis",
        "select_asset": "Select Asset",
        "score_help": "Risk-adjusted score",
        "signals_header": "AI Signals & Reasoning",
        "no_signals": "No strong signals detected.",
        "comparison_subheader": "Performance Comparison",
        "select_compare": "Select assets to compare",
        "metric_score": "Score",
        "metric_recommendation": "Recommendation",
        "metric_max_dd": "Max Drawdown",
        "col_ticker": "Ticker",
        "col_price": "Price",
        "col_return": "Return",
        "col_vol": "Vol (Ann.)",
        "col_rsi": "RSI",
        "tab_assistant": "🤖 Assistant",
        "bot_welcome": "Hello! I am your financial assistant. I can explain the analysis of any asset in your list.",
        "bot_placeholder": "Ask me about a ticker (e.g. Why AAPL?)",
        
        # Bot Templates (English)
        "bot_buy_recommendation": """
### Analysis for **{ticker}**

Based on the analysis, I recommend **BUYING** this asset with a score of **{score}/100**.

**Why?**
{reasoning}

The technical indicators are positive, showing strong momentum (RSI: {rsi}) and acceptable volatility. This suggests a potential uptrend aligned with your risk profile.
""",
        "bot_hold_recommendation": """
### Analysis for **{ticker}**

I recommend **HOLDING** this position (Score: **{score}/100**).

**Context:**
{reasoning}

The market signals are mixed right now. The RSI is at **{rsi}**, indicating no clear overbought or oversold conditions. It is better to wait for a clearer trend confirmation before increasing your position.
""",
        "bot_sell_recommendation": """
### Analysis for **{ticker}**

CAUTION: The recommendation is to **SELL** (Score: **{score}/100**).

**Risk Factors:**
{reasoning}

Technical indicators suggest a downtrend or overvaluation (RSI: {rsi}). It might be a good time to take profits or cut losses to protect your capital.
""",
    },
    "es": {
        "title": "FinanceLab: Analizador de Mercado y Screener de CEDEARs",
        "description": "Análisis técnico profesional y puntaje de riesgo para gestión de portafolios.",
        "config_header": "Configuración",
        "language": "Idioma",
        "risk_profile": "Perfil de Riesgo",
        "risk_profile_help": "Determina cómo el motor de puntuación pondera la volatilidad vs el momentum.",
        "analysis_period": "Período de Análisis",
        "watchlist": "Lista de Seguimiento (separada por comas)",
        "analyze_btn": "Analizar Mercado",
        "about": "Acerca de",
        "about_text": "Construido con Python, Streamlit, yFinance y Plotly.",
        "disclaimer_title": "⚠️ Aviso Legal",
        "disclaimer_text": "Esta aplicación es solo para fines informativos y no constituye asesoramiento financiero. Las inversiones conllevan riesgos, incluida la posible pérdida del capital. Los creadores de esta aplicación no se hacen responsables de ninguna pérdida financiera.",
        "spinner": "Obteniendo datos y calculando puntajes...",
        "warning_fetch": "No se pudieron obtener datos para {}",
        "tab_ranking": "📊 Ranking Resumido",
        "tab_detail": "🔎 Detalle del Activo",
        "tab_comparison": "📈 Comparación",
        "ranking_subheader": "Ranking de Activos ({} activos)",
        "download_csv": "Descargar Reporte (CSV)",
        "deep_dive_subheader": "Análisis Detallado",
        "select_asset": "Seleccionar Activo",
        "score_help": "Puntaje ajustado por riesgo",
        "signals_header": "Señales IA y Razonamiento",
        "no_signals": "No se detectaron señales fuertes.",
        "comparison_subheader": "Comparación de Rendimiento",
        "select_compare": "Seleccionar activos para comparar",
        "metric_score": "Puntaje",
        "metric_recommendation": "Recomendación",
        "metric_max_dd": "Caída Máx.",
        "col_ticker": "Ticker",
        "col_price": "Precio",
        "col_return": "Retorno",
        "col_vol": "Vol (Anual)",
        "col_rsi": "RSI",
        "tab_assistant": "🤖 Asistente",
        "bot_welcome": "¡Hola! Soy tu Asistente Financiero. Puedo explicar los resultados del análisis o responder preguntas sobre los activos. Intenta preguntar: '¿Por qué comprar AAPL?'",
        "bot_placeholder": "Pregunta sobre un activo (ej: 'Estado de TSLA')",
        "bot_error_no_context": "Por favor, ejecuta 'Analizar Mercado' primero para tener datos sobre los cuales conversar.",
        "bot_unknown_ticker": "No encontré análisis para '{}'. Asegúrate de que estaba en la lista de seguimiento.",
        "bot_buy_recommendation": """
### Análisis para **{ticker}**

Basado en el análisis, recomiendo **COMPRAR** este activo con un puntaje de **{score}/100**.

**¿Por qué?**
{reasoning}

Los indicadores técnicos son positivos, mostrando un momentum fuerte (RSI: {rsi}) y una volatilidad aceptable. Esto sugiere una tendencia alcista alineada con tu perfil de riesgo.
""",
        "bot_hold_recommendation": """
### Análisis para **{ticker}**

Recomiendo **MANTENER** o esperar en este activo (Puntaje: **{score}/100**).

**Contexto:**
{reasoning}

Las señales actuales son mixtas. El RSI está en {rsi}, lo que indica indecisión o una tendencia neutral. Es más seguro esperar una señal de entrada más clara.
""",
        "bot_sell_recommendation": """
### Análisis para **{ticker}**

Mi recomendación es **VENDER** o evitar este activo (Puntaje: **{score}/100**).

**Factores de Riesgo:**
{reasoning}

Los indicadores técnicos sugieren presión a la baja o riesgo excesivo. El RSI ({rsi}) sugiere una tendencia bajista.
"""
    }
}

def get_text(lang: str, key: str) -> str:
    """Retrieve translated text for a given key."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
