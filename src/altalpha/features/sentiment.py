import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

def score_text(text: str) -> float:
    """Return VADER 'compound' sentiment score in [-1, 1]."""
    return _analyzer.polarity_scores(text)["compound"]

def daily_sentiment(posts: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate per-post sentiments into daily features.
    Returns columns ['sent_mean', 'sent_median', 'n_posts'] at daily frequency.
    """
    df = posts.copy()
    df["sent"] = df["text"].map(score_text)
    daily = df.resample("1D")["sent"].agg(["mean", "median", "count"])
    daily = daily.fillna(method="ffill")
    daily = daily.rename(columns={"mean": "sent_mean", "median": "sent_median", "count": "n_posts"})
    return daily
