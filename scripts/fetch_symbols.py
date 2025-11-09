# scripts/fetch_symbols.py
import os
import pandas as pd
import requests
from io import StringIO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SYM_DIR = BASE_DIR / "data" / "symbols"
SYM_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = SYM_DIR / "nifty500_yf.csv"

def main():
    print(" Fetching NSE 500 tickers from NSE India (official API)...")
    url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        session = requests.Session()
        r = session.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        data = r.json()["data"]

        df = pd.DataFrame(data)
        df["symbol"] = df["symbol"].astype(str).str.strip() + ".NS"
        df[["symbol"]].to_csv(OUT_CSV, index=False)
        print(f" Saved {len(df)} Yahoo Finance tickers → {OUT_CSV}")

    except Exception as e:
        print(f" Could not download official NIFTY 500 list ({e})")
        fallback = [
            "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
            "ITC.NS","LT.NS","HINDUNILVR.NS","SBIN.NS","BHARTIARTL.NS",
            "KOTAKBANK.NS","AXISBANK.NS","ASIANPAINT.NS","ADANIENT.NS",
            "ADANIPORTS.NS","M&M.NS","MARUTI.NS","TATAMOTORS.NS","TATASTEEL.NS",
            "TATAPOWER.NS","TATACONSUM.NS","TITAN.NS","ULTRACEMCO.NS",
            "SUNPHARMA.NS","CIPLA.NS","WIPRO.NS","TECHM.NS","NTPC.NS","ONGC.NS",
            "COALINDIA.NS","POWERGRID.NS","BAJFINANCE.NS","BAJAJFINSV.NS",
            "SBILIFE.NS","HDFCLIFE.NS","JSWSTEEL.NS","GRASIM.NS","DRREDDY.NS",
            "INDIGO.NS","NESTLEIND.NS","TRENT.NS","EICHERMOT.NS","BEL.NS",
            "BAJAJ-AUTO.NS","MAXHEALTH.NS","HCLTECH.NS","SHRIRAMFIN.NS",
            "TATACOMM.NS","IRCTC.NS","POLYCAB.NS"
        ]
        pd.DataFrame({"symbol": fallback}).to_csv(OUT_CSV, index=False)
        print(f"Saved fallback tickers → {OUT_CSV}")

if __name__ == "__main__":
    main()
