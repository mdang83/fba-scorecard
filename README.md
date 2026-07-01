# FBA Product Opportunity Scorecard

A data-driven dashboard that scores Amazon product niches using live Google Trends data, Reddit community buzz, and BSR-derived sales estimates — helping sellers identify high-potential opportunities before entering a market.

🔗 **[Live Demo](https://fba-scorecard.streamlit.app)**

---

## Overview

Entering the wrong Amazon niche is one of the most common FBA mistakes. This tool aggregates three independent signals into a single **Opportunity Score (0–100)** so sellers can compare niches objectively and prioritize research.

---

## Features

- 🔍 **Keyword search** — enter any product niche to analyze
- 📈 **Google Trends integration** — 12-month interest trend via `pytrends`
- 💬 **Reddit buzz tracking** — mention volume from r/fulfillmentbyamazon and r/amazonseller
- 📦 **BSR-to-sales estimator** — estimates monthly unit sales from Best Seller Rank
- 🎯 **Weighted Opportunity Score** — combines all signals into a single 0–100 score
- 📊 **Opportunity Score gauge** - color-coded visual gauge with per-signal metric cards (Trend, Buzz, Sales)
- 🟢 Color-coded output — green (>70), yellow (40–70), red (<40)

---

## Scoring Methodology

| Signal                      | Weight | Normalization                                                        |
| ---------------------------- | ------ | --------------------------------------------------------------------- |
| Google Trends avg (0–100)    | 40%    | Direct — already 0–100                                                |
| Reddit mentions (30 days)    | 30%    | Log scale — 50 mentions ≈ 100, 1 mention ≈ 29, 0 → 0                  |
| Est. monthly sales from BSR  | 30%    | Log scale — anchored to a BSR=1 ceiling of ~25,000 units/month        |

**BSR → Sales formula:** `estimated_monthly_sales = 25000 / (BSR ^ 0.7)`

Calibrated to competitive categories (e.g. Home & Kitchen):
- BSR 100 ≈ 995 units/month
- BSR 1,000 ≈ 199 units/month
- BSR 5,000 ≈ 64 units/month
- BSR 50,000 ≈ 13 units/month

**Final score:** `opportunity_score = (trend × 0.40) + (buzz × 0.30) + (sales × 0.30)`

---

## Tech Stack

- **Python** — core logic and data processing
- **Streamlit** — dashboard UI
- **Plotly** — radar chart and trend line visualizations
- **pytrends** — Google Trends API wrapper
- **PRAW** — Reddit API client
- **pandas / numpy** — data manipulation

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/mdang83/fba-scorecard.git
cd fba-scorecard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Add Reddit credentials
Create `.streamlit/secrets.toml`:
```toml
[reddit]
client_id = "your_client_id"
client_secret = "your_client_secret"
user_agent = "fba-scorecard/1.0 by your_username"
```
Get free credentials at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps). Without them, Buzz Score defaults to 0.

### 4. Run the app
```bash
streamlit run app.py
```

---

## Project Structure

```
fba-scorecard/
├── app.py              # Main Streamlit dashboard
├── scorer.py           # Scoring engine (normalization + weighting)
├── data/
│   └── fetcher.py      # Google Trends and Reddit data fetching
├── requirements.txt
└── .streamlit/
    └── secrets.toml.example
```

---

## Author

**Morrice Dang**  
B.S. Applied Data Science — California State University, Long Beach  
[GitHub](https://github.com/mdang83)
