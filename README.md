# FinanceLab: Market Analyzer & CEDEAR Screener

Una aplicación profesional en Python para el análisis técnico y fundamental de activos financieros (Acciones, CEDEARs, ETFs), optimizada para la toma de decisiones basada en perfiles de riesgo.

## 🚀 Características

- **Dashboard Interactivo**: Construido con Streamlit.
- **Análisis Multi-Activo**: Soporte para cualquier ticker disponible en Yahoo Finance.
- **Motor de Scoring**: Clasificación de activos (0-100) basada en:
  - **Tendencia**: Cruces de medias (SMA 50/200).
  - **Momentum**: RSI (Relative Strength Index).
  - **Riesgo**: Volatilidad anualizada y Max Drawdown.
- **Perfiles de Riesgo**: Ajuste dinámico del scoring según perfil (Conservador, Moderado, Agresivo).
- **Caching Inteligente**: Sistema de caché local (SQLite + Parquet) para minimizar llamadas a API y mejorar performance.

## 🛠️ Stack Tecnológico

- **Core**: Python 3.11+
- **Datos**: `yfinance`, `pandas`, `numpy`
- **UI**: `streamlit`, `plotly`
- **Almacenamiento**: `sqlite3`
- **Calidad**: `pytest`, Type hints

## ⚙️ Instalación y Configuración

1. **Clonar el repositorio** (o descargar los archivos):
   ```bash
   git clone <repo-url>
   cd FinanceLab
   ```

2. **Crear entorno virtual (Recomendado)**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuración de entorno**:
   Copiar el archivo de ejemplo y ajustar si es necesario.
   ```bash
   copy .env.example .env
   ```

## ▶️ Ejecución

Para iniciar el dashboard:

```bash
streamlit run src/app/main.py
```

La aplicación se abrirá automáticamente en tu navegador (usualmente en `http://localhost:8501`).

## 🧪 Tests

El proyecto incluye tests unitarios para la capa de datos y el motor de análisis.

```bash
pytest
```
*Nota: Si `pytest` no está en el path, asegúrate de haber instalado las dependencias en el entorno virtual activo.*

## 📂 Estructura del Proyecto

```text
FinanceLab/
├── src/
│   ├── app/            # Capa de Presentación (Streamlit)
│   ├── data/           # Capa de Datos (Loader & Cache)
│   ├── domain/         # Logica de Negocio (Signals, Models)
│   └── analysis/       # Biblioteca de Indicadores y Métricas
├── tests/              # Tests Unitarios
├── requirements.txt    # Dependencias
└── README.md           # Documentación
```

## 📝 Notas de Diseño

- **Arquitectura**: Se separó claramente la UI (`src/app`) de la lógica de dominio (`src/domain` y `src/analysis`) para facilitar el testing y futuro mantenimiento.
- **Cache**: Se implementó un caché con TTL (Time-To-Live) para evitar bloqueos por rate-limit de la API de Yahoo Finance y mejorar la velocidad de carga en segundas consultas.
- **Extensibilidad**: El sistema de scoring está desacoplado, permitiendo agregar nuevos indicadores o cambiar las ponderaciones fácilmente en `SignalEngine`.
