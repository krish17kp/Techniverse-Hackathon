# scripts/grid_search.py
import os, itertools, pandas as pd
from strategy import run_symbol, DATA_DIR, RESULT_DIR

SHORTS=[5,10,20]; LONGS=[30,50,100]; TYPES=["EMA","SMA","WMA"]

def main():
    base=os.path.dirname(__file__)
    data=os.path.join(base,DATA_DIR)
    out=os.path.join(base,RESULT_DIR)
    os.makedirs(out,exist_ok=True)
    files=[f for f in os.listdir(data) if f.endswith(".csv")]
    rows=[]
    for f in files:
        best=None
        for s,l,t in itertools.product(SHORTS,LONGS,TYPES):
            if s>=l: continue
            m,_,_=run_symbol(f,s,l,t)
            if not m: continue
            cand={"symbol":f.replace(".csv",""),"ma_type":t,"short":s,"long":l,**m}
            if best is None or cand["total_return_pct"]>best["total_return_pct"]: best=cand
        if best: rows.append(best)
    if rows: pd.DataFrame(rows).to_csv(os.path.join(out,"grid_best_per_symbol.csv"),index=False)
    print(" Grid search done")

if __name__=="__main__": main()
