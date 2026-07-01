import time
import pandas as pd
from pytrends.request import TrendReq


def fetch_google_trends(keyword: str) -> dict:
    """Fetch Google Trends interest over time for the last 12 months."""
    try:
        pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25))
        pytrends.build_payload([keyword], timeframe="today 12-m", geo="US")
        df = pytrends.interest_over_time()

        if df.empty or keyword not in df.columns:
            return {"average": 0.0, "data": pd.DataFrame()}

        series = df[keyword].copy()
        return {"average": float(series.mean()), "data": series.to_frame()}
    except Exception as e:
        return {"average": 0.0, "data": pd.DataFrame(), "error": str(e)}


def fetch_reddit_mentions(
    keyword: str, client_id: str, client_secret: str, user_agent: str
) -> dict:
    """Count posts mentioning the keyword in FBA subreddits from the last 30 days."""
    import praw

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

        subreddits = ["fulfillmentbyamazon", "amazonseller"]
        cutoff = time.time() - (30 * 24 * 60 * 60)
        total = 0

        for sub_name in subreddits:
            subreddit = reddit.subreddit(sub_name)
            results = subreddit.search(
                keyword, sort="new", time_filter="month", limit=250
            )
            for post in results:
                if post.created_utc >= cutoff:
                    total += 1

        return {"mentions": total}
    except Exception as e:
        return {"mentions": 0, "error": str(e)}


def estimate_monthly_sales(bsr: int) -> float:
    """Estimate monthly unit sales from BSR using: 25000 / (BSR ^ 0.7).
    Calibrated to competitive categories (e.g. Home & Kitchen).
    BSR 100 ≈ 995, BSR 1000 ≈ 199, BSR 5000 ≈ 64, BSR 50000 ≈ 13.
    """
    if bsr <= 0:
        return 0.0
    return 25000.0 / (bsr**0.7)
