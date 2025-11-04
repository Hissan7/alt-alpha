import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))


import argparse
from pathlib import Path
import pandas as pd

from altalpha.config import DATA_PROCESSED
from altalpha.data.price import fetch_daily_prices
from altalpha.data.altdata import load_posts_csv
from altalpha.features.sentiment import daily_sentiment

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--start", required=True)  # YYYY-MM-DD
    ap.add_argument("--end", required=True)    # YYYY-MM-DD
    ap.add_argument("--altcsv", required=True, help="Path to raw posts CSV (created_utc,text)")
    args = ap.parse_args()

    # 1) Load raw posts and compute daily sentiment (calendar days, includes weekends/holidays)
    posts = load_posts_csv(args.altcsv)
    sent = daily_sentiment(posts)  # index = calendar date (UTC), cols: sent_mean/sent_median/n_posts

    # 2) Load trading-day prices/returns from Yahoo Finance
    px = fetch_daily_prices(args.ticker, args.start, args.end)  # index = trading days, cols: close, ret

    # 3) Build a daily calendar index covering the union of sentiment + price date ranges
    cal_start = min(sent.index.min().date(), px.index.min().date()) if not sent.empty else px.index.min().date()
    cal_end   = max(sent.index.max().date(), px.index.max().date()) if not sent.empty else px.index.max().date()
    cal_index = pd.date_range(cal_start, cal_end, freq="D", tz="UTC")

    # 4) Reindex prices to the full calendar and forward-fill 'close' so weekends/holidays have last known price
    px_cal = px.copy()
    # make the price index timezone-aware UTC to match sentiment
    px_cal.index = pd.to_datetime(px_cal.index, utc=True)
    px_cal = px_cal.reindex(cal_index).ffill()

    # 5) Compute the NEXT-day return on the calendar index:
    #    next_ret = close[t+1] / close[t] - 1
    #    This maps sentiment on day t to the market move on the next available day.
    px_cal["next_ret"] = px_cal["close"].shift(-1) / px_cal["close"] - 1
    # keep original trading-day 'ret' too (optional, useful for diagnostics)
    # but we’ll use 'next_ret' in backtests for no-lookahead.
    # Fill any trailing NaN (last day has no next day) with 0
    px_cal["next_ret"] = px_cal["next_ret"].fillna(0.0)

    # 6) Merge calendar prices with daily sentiment on the calendar index (outer join via reindex above)
    merged = px_cal.join(sent, how="left")

    # 7) Fill missing sentiment on days with no posts: neutral sentiment (0) and zero count
    merged["sent_mean"]   = merged["sent_mean"].fillna(0.0)
    merged["sent_median"] = merged["sent_median"].fillna(0.0)
    merged["n_posts"]     = merged["n_posts"].fillna(0).astype(int)

    # 8) Save to data/processed/<TICKER>_daily.csv (index name 'date')
    outpath = DATA_PROCESSED / f"{args.ticker}_daily.csv"
    merged.index.name = "date"
    merged.to_csv(outpath)
    print(f"[OK] Saved merged dataset to {outpath}")
    print(merged.head(10))

if __name__ == "__main__":
    main()
