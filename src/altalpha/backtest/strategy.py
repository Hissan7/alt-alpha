import pandas as pd

def generate_positions(signal: pd.Series, pos_thresh=0.1, neg_thresh=-0.1) -> pd.Series:
    """
    +1 if signal > pos_thresh, 0 if within band, -1 if signal < neg_thresh.
    """
    pos = pd.Series(0.0, index=signal.index)
    pos[signal > pos_thresh] = 1.0
    pos[signal < neg_thresh] = -1.0
    return pos

def run_backtest(daily: pd.DataFrame, signal_col="sent_mean",
                 pos_thresh=0.1, neg_thresh=-0.1, trading_cost_bp=5) -> pd.DataFrame:
    """
    Daily backtest using next-day returns. Produces strategy columns and equity.
    """
    df = daily.copy()
    if "ret" not in df.columns:
        raise ValueError("Input 'daily' must include a 'ret' column (daily returns).")
    if signal_col not in df.columns:
        raise ValueError(f"Missing signal column '{signal_col}' in input dataframe.")

    df["signal"] = df[signal_col]
    df["position"] = generate_positions(df["signal"], pos_thresh, neg_thresh)

    df["pos_change"] = df["position"].diff().abs().fillna(0.0)
    cost_per_unit = trading_cost_bp / 10000.0
    cost = cost_per_unit * df["pos_change"]

    df["ret_shifted"] = df["ret"].shift(-1).fillna(0.0)
    df["strategy_ret_gross"] = df["position"] * df["ret_shifted"]
    df["strategy_ret_net"] = df["strategy_ret_gross"] - cost
    df["strategy_equity"] = (1 + df["strategy_ret_net"]).cumprod()
    return df
