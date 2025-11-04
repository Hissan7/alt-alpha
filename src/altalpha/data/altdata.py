import pandas as pd
from altalpha.utils import ensure_datetime_index

def load_posts_csv(path: str) -> pd.DataFrame:
    """
    Load a CSV of posts with at least ['created_utc', 'text'].
    Returns a DataFrame indexed by UTC datetime with a 'text' column.
    """
    df = pd.read_csv(path)
    required = {"created_utc", "text"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")
    df = ensure_datetime_index(df, "created_utc")
    df["text"] = df["text"].astype(str).fillna("")
    return df[["text"]]
