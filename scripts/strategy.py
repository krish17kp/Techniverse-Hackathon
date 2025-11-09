import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/eod")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "../results")
os.makedirs(RESULTS_DIR, exist_ok=True)

SHORT_MA = 10
LONG_MA = 50

def backtest(symbol):
    file_path = os.path.join(DATA_DIR, f"{symbol}.csv")
    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)
    df["MA_Short"] = df["Close"].rolling(SHORT_MA).mean()
    df["MA_Long"] = df["Close"].rolling(LONG_MA).mean()
    df.dropna(inplace=True)

    # Generate signals
    df["Signal"] = np.where(df["MA_Short"] > df["MA_Long"], 1, 0)
    df["Position"] = df["Signal"].diff()

    # Track returns
    df["Daily_Return"] = df["Close"].pct_change()
    df["Strategy_Return"] = df["Signal"].shift(1) * df["Daily_Return"]

    total_return = (df["Strategy_Return"] + 1).prod() - 1
    win_rate = (df["Strategy_Return"] > 0).mean() * 100
    trades = df["Position"].abs().sum()
    max_dd = ((df["Close"] / df["Close"].cummax()) - 1).min()

    return {
        "Stock": symbol,
        "Total Return (%)": round(total_return * 100, 2),
        "Win Rate (%)": round(win_rate, 2),
        "Trades": int(trades),
        "Max Drawdown (%)": round(max_dd * 100, 2),
    }

def main():
    results = []
    for f in os.listdir(DATA_DIR):
        if f.endswith(".csv"):
            symbol = f.replace(".csv", "")
            res = backtest(symbol)
            if res:
                results.append(res)

    if results:
        df_summary = pd.DataFrame(results)
        out_path = os.path.join(RESULTS_DIR, "summary.csv")
        df_summary.to_csv(out_path, index=False)
        print(f"✅ Backtest completed. Summary saved at {out_path}")
        print(df_summary)
    else:
        print("⚠️ No data available to backtest.")

if __name__ == "__main__":
    main()
