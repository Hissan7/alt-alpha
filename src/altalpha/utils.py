import pandas as pd

def ensure_datetime_index(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Convert a dataframe column to timezone-aware UTC datetime and set it as index.
    """
    df = df.copy()  # don't mutate caller's DataFrame
    df[col] = pd.to_datetime(df[col], utc=True, errors="coerce")
    df = df.dropna(subset=[col]).sort_values(col)
    df = df.set_index(col)
    return df
