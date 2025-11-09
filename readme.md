# 📈 Moving Average Crossover Hackathon Project

This project implements a **Moving Average Crossover Strategy** on NSE stocks (dummy or API data) and visualizes results in a Streamlit dashboard.

## 📊 Components

- `data_fetch.py`: Fetches or generates 3-month price data.
- `strategy.py`: Backtests MA crossover strategy.
- `app.py`: Streamlit dashboard visualization.

## 🚀 Run Locally

```bash
pip install -r requirements.txt
python scripts/data_fetch.py
python scripts/strategy.py
streamlit run app.py
```
