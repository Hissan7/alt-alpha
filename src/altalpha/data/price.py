import pandas as pd
import yfinance as yf

def fetch_daily_prices(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Fetch daily adjusted close prices and compute daily returns.
    Returns columns: ['adj close', 'ret'] with index named 'date'.
    """
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df is None or df.empty:
        raise ValueError(f"No price data for {ticker} between {start} and {end}")
    df = df.rename(columns=str.lower)
    df.index.name = "date"
    df["ret"] = df["close"].pct_change().fillna(0.0)
    return df[["close", "ret"]]
