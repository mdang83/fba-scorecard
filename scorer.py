import math


def _trend_score(average_interest: float) -> float:
    """Google Trends is already 0–100; clamp and return directly."""
    return max(0.0, min(100.0, average_interest))


def _buzz_score(mentions: int) -> float:
    """Log-normalize Reddit mentions.
    50 mentions → ~100; 1 mention → ~29; 0 → 0.
    Log scale prevents a few viral posts from dominating.
    """
    if mentions <= 0:
        return 0.0
    score = math.log10(mentions + 1) / math.log10(51) * 100
    return max(0.0, min(100.0, score))


def _sales_score(estimated_sales: float) -> float:
    """Log-normalize estimated monthly sales.
    Anchored to the BSR=1 ceiling of ~3000 units.
    BSR≈10 (~600 units) → ~86; BSR≈100 (~120 units) → ~70; BSR≈10k (~5 units) → ~38.
    """
    if estimated_sales <= 0:
        return 0.0
    score = math.log10(estimated_sales + 1) / math.log10(3001) * 100
    return max(0.0, min(100.0, score))


def calculate_opportunity_score(
    trend_avg: float, reddit_mentions: int, estimated_sales: float
) -> dict:
    trend = _trend_score(trend_avg)
    buzz = _buzz_score(reddit_mentions)
    sales = _sales_score(estimated_sales)

    opportunity = trend * 0.40 + buzz * 0.30 + sales * 0.30

    return {
        "opportunity_score": round(opportunity, 1),
        "trend_score": round(trend, 1),
        "buzz_score": round(buzz, 1),
        "sales_score": round(sales, 1),
    }
