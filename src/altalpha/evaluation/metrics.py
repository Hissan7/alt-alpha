import numpy as np
import pandas as pd

def sharpe(returns: pd.Series, risk_free_daily: float = 0.0) -> float:
    r = returns - risk_free_daily
    vol = r.std(ddof=0)
    if vol == 0 or np.isnan(vol):
        return 0.0
    return np.sqrt(252) * r.mean() / vol

def max_drawdown(equity: pd.Series) -> float:
    peak = equity.cummax()
    dd = (equity / peak) - 1.0
    return float(dd.min())

def cagr(equity: pd.Series, periods_per_year: int = 252) -> float:
    if len(equity) == 0:
        return 0.0
    start, end = float(equity.iloc[0]), float(equity.iloc[-1])
    if start <= 0:
        return 0.0
    total_return = end / start - 1.0
    years = len(equity) / periods_per_year
    if years <= 0:
        return 0.0
    return (1 + total_return) ** (1 / years) - 1
