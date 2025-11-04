# Alt Alpha

Alt Alpha is a quantitative research and trading intelligence platform that combines alternative data, sentiment analysis, and backtesting to evaluate trading strategies.  
It is designed for experimentation, feature engineering, and performance evaluation using a modular Python-based architecture.

---

# Features

- Alternative Data Integration** – Collects and processes non-traditional datasets such as Reddit sentiment, news, and market data. 

- Feature Engineering** – Extracts meaningful features from sentiment and price data for predictive modeling.

- Backtesting Engine** – Simulates trading strategies over historical data to measure performance. 

- Evaluation Metrics** – Provides quantitative evaluation tools such as Sharpe Ratio, Sortino Ratio, and drawdown statistics. 

- Configurable Architecture** – Flexible configuration system for easy experiment management.  

- Extensible Design** – Modular structure for adding new data sources, strategies, and evaluation criteria.

---

# Project Structure

alt-alpha/
├── data/ # Datasets and raw data files
├── notes.txt # Development notes and logs
├── scripts/ # One-off scripts (e.g., dataset builders)
│ └── build_dataset.py
├── src/
│ └── altalpha/
│ ├── backtest/ # Strategy testing and simulation
│ ├── config.py # Global configurations
│ ├── data/ # Data ingestion and processing
│ ├── evaluation/ # Performance metrics and reports
│ ├── features/ # Feature extraction modules
│ └── utils.py # Utility functions
└── .venv/ # Virtual environment (not tracked in Git)

---

# Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/alt-alpha.git
   cd alt-alpha

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate
    Install dependencies:
    pip install -r requirements.txt

Usage


Build Dataset

    python scripts/build_dataset.py

Run Backtest
    python -m src.altalpha.backtest.strategy

Evaluate Strategy

    python -m src.altalpha.evaluation.metrics

Example Workflow

    - Configure parameters in src/altalpha/config.py
    - Generate datasets with alternative data
    - Extract sentiment and price features
    - Run backtests with different strategy parameters
    - Analyze metrics to optimize performance


Tech Stack

- Python 3.11+
- NumPy, Pandas, Scikit-learn
- Matplotlib, Seaborn
- Yahoo Finance API or custom data ingestion


Author

Hissan Omar
MSc Artificial Intelligence, King’s College London
London, United Kingdom
Focus Areas: Quantitative Research, Machine Learning, Financial AI