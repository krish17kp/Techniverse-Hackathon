import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/eod")
SYMBOLS_CSV = os.path.join(os.path.dirname(__file__), "../data/symbols/nifty500_yf.csv")

def fetch_symbol(symbol, period="3mo", interval="1d"):
    try:
        df = yf.download(symbol, period=period, interval=interval, progress=False)
        if df.empty:
            return pd.DataFrame()
        df = df.reset_index()[["Date","Close"]]
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        return df.dropna(subset=["Close"])
    except Exception as e:
        print(f"!! {symbol} error: {e}")
        return pd.DataFrame()

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(SYMBOLS_CSV):
        print("Symbols list missing. Run fetch_symbols first.")
        return
    symbols = pd.read_csv(SYMBOLS_CSV)["symbol"].dropna().tolist()
    ok = skip = 0
    total = len(symbols)
    for i, sym in enumerate(symbols, 1):
        print(f"[{i}/{total}] {sym} …", end="")
        df = fetch_symbol(sym)
        if df.empty or len(df) < 20:  # minimal length
            print(" skipped")
            skip += 1
        else:
            out = os.path.join(DATA_DIR, f"{sym}.csv")
            df.to_csv(out, index=False)
            print(" OK")
            ok += 1
        time.sleep(0.5)
    print(f"Done. OK: {ok}, Skipped: {skip}")
