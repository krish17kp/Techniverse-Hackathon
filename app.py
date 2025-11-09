# app.py
import os
import pandas as pd
import streamlit as st
import plotly.graph_objs as go

DATA_DIR = "data/eod"
RESULTS_DIR = "results"

st.set_page_config(page_title="MA Crossover Dashboard", layout="wide")
st.title("📊 Moving Average Crossover Strategy Dashboard")

# Load available symbols
try:
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
except Exception as e:
    st.error(f"Data directory not found or inaccessible: {e}")
    st.stop()

if not files:
    st.error("No data files found. Please run the data_fetch script.")
    st.stop()

symbols = sorted([f.replace(".csv", "") for f in files])
symbol = st.selectbox("Select Stock Symbol", symbols)

# Load symbol data
symbol_path = os.path.join(DATA_DIR, f"{symbol}.csv")
try:
    df = pd.read_csv(symbol_path)
except Exception as e:
    st.error(f"Could not read data for {symbol}: {e}")
    st.stop()

if df.empty or "Date" not in df.columns or "Close" not in df.columns:
    st.error(f"Data for {symbol} is empty or invalid. Please check the CSV.")
    st.stop()

short = st.number_input("Short MA Period", min_value=5, max_value=50, value=10, step=1)
long = st.number_input("Long MA Period", min_value=20, max_value=200, value=50, step=1)

# Convert Date column to datetime
try:
    df["Date"] = pd.to_datetime(df["Date"])
except Exception:
    pass

df = df.sort_values("Date")

# Compute MAs
df["MA_short"] = df["Close"].rolling(window=short).mean()
df["MA_long"] = df["Close"].rolling(window=long).mean()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name="Close"))
fig.add_trace(go.Scatter(x=df["Date"], y=df["MA_short"], mode="lines", name=f"MA {short}"))
fig.add_trace(go.Scatter(x=df["Date"], y=df["MA_long"], mode="lines", name=f"MA {long}"))
fig.update_layout(template="plotly_white", xaxis_title="Date", yaxis_title="Price")
st.plotly_chart(fig, width=None, use_container_width=True)

# Load summary
summary_path = os.path.join(RESULTS_DIR, "summary.csv")
if os.path.exists(summary_path):
    try:
        summary = pd.read_csv(summary_path)
    except pd.errors.EmptyDataError:
        st.warning("Summary file is empty or corrupted. Run strategy.py to generate it.")
        summary = None
    except Exception as e:
        st.error(f"Error reading summary file: {e}")
        summary = None

    if summary is not None:
        if summary.empty or summary.columns.size == 0:
            st.warning("Summary file has no data. Run strategy.py and grid_search.py.")
        else:
            st.subheader("Backtest Summary")
            st.dataframe(summary)
else:
    st.info("No summary file found. Run strategy.py to generate back‐test results.")
