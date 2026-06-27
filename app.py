import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from data.fetcher import fetch_google_trends, fetch_reddit_mentions, estimate_monthly_sales
from scorer import calculate_opportunity_score

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FBA Product Opportunity Scorecard",
    page_icon="📦",
    layout="wide",
)

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        .block-container { padding-top: 2rem; }
        div[data-testid="metric-container"] {
            background: #1e1e2e;
            border: 1px solid #313244;
            border-radius: 10px;
            padding: 16px 20px;
        }
        div[data-testid="metric-container"] label { color: #cdd6f4 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown(
        """
        1. **Enter a product keyword** — e.g. *bamboo cutting board*
        2. **Enter the BSR** from an Amazon competitor's listing
        3. Click **Analyze Opportunity**

        ---

        **Score thresholds**

        | Score | Signal |
        |-------|--------|
        | 🟢 > 70 | Strong opportunity |
        | 🟡 40 – 70 | Moderate opportunity |
        | 🔴 < 40 | Weak opportunity |

        ---

        **What each signal measures**

        - **Trend Score (40%)** — average Google search interest over the last 12 months (0–100 scale)
        - **Buzz Score (30%)** — Reddit post volume in r/fulfillmentbyamazon and r/amazonseller over the last 30 days
        - **Sales Potential (30%)** — estimated monthly unit sales derived from BSR using `3000 ÷ BSR^0.7`

        ---

        **Reddit credentials**

        Add a `.streamlit/secrets.toml` file in this project:

        ```toml
        [reddit]
        client_id     = "your_client_id"
        client_secret = "your_client_secret"
        user_agent    = "fba-scorecard/1.0"
        ```

        Get free credentials at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).
        Without them the Buzz Score defaults to 0.
        """
    )

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📦 FBA Product Opportunity Scorecard")
st.markdown(
    "Score any Amazon product niche in seconds using live Google Trends data, "
    "Reddit community buzz, and BSR-derived sales estimates."
)
st.divider()

# ── Inputs ────────────────────────────────────────────────────────────────────
col_kw, col_bsr, col_btn = st.columns([3, 2, 1.2])
with col_kw:
    keyword = st.text_input(
        "Product Keyword",
        placeholder="e.g. bamboo cutting board",
        label_visibility="visible",
    )
with col_bsr:
    bsr = st.number_input(
        "Best Seller Rank (BSR)",
        min_value=1,
        max_value=10_000_000,
        value=5_000,
        step=500,
    )
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze = st.button("🔍 Analyze", type="primary", use_container_width=True)

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze:
    if not keyword.strip():
        st.error("Please enter a product keyword before analyzing.")
        st.stop()

    # Detect Reddit credentials
    reddit_ok = False
    try:
        rc = st.secrets.get("reddit", {})
        if rc.get("client_id") and rc.get("client_secret") and rc.get("user_agent"):
            reddit_ok = True
    except Exception:
        pass

    if not reddit_ok:
        st.warning(
            "Reddit API credentials not found — Buzz Score will be 0. "
            "See the sidebar for setup instructions."
        )

    with st.spinner("Fetching live data…"):
        trends_result = fetch_google_trends(keyword.strip())

        if reddit_ok:
            reddit_result = fetch_reddit_mentions(
                keyword.strip(),
                st.secrets["reddit"]["client_id"],
                st.secrets["reddit"]["client_secret"],
                st.secrets["reddit"]["user_agent"],
            )
        else:
            reddit_result = {"mentions": 0}

        est_sales = estimate_monthly_sales(bsr)
        scores = calculate_opportunity_score(
            trends_result["average"],
            reddit_result["mentions"],
            est_sales,
        )

    opp = scores["opportunity_score"]

    if opp >= 70:
        color, label, badge = "#2ecc71", "Strong Opportunity", "🟢"
    elif opp >= 40:
        color, label, badge = "#f39c12", "Moderate Opportunity", "🟡"
    else:
        color, label, badge = "#e74c3c", "Weak Opportunity", "🔴"

    st.divider()

    # ── Opportunity Score card ────────────────────────────────────────────────
    card_col, spacer = st.columns([1, 2])
    with card_col:
        st.markdown(
            f"""
            <div style="
                background: {color}18;
                border: 2px solid {color};
                border-radius: 18px;
                padding: 28px 24px;
                text-align: center;
            ">
                <div style="font-size: 4rem; font-weight: 800; color: {color}; line-height: 1;">
                    {opp}
                </div>
                <div style="font-size: 1.15rem; font-weight: 600; color: {color}; margin-top: 6px;">
                    {badge} {label}
                </div>
                <div style="font-size: 0.85rem; color: #888; margin-top: 4px;">
                    Opportunity Score out of 100
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Charts row ────────────────────────────────────────────────────────────
    left, right = st.columns(2)

    with left:
        st.subheader("Sub-Score Radar")
        categories = ["Trend Score", "Buzz Score", "Sales Potential"]
        values = [scores["trend_score"], scores["buzz_score"], scores["sales_score"]]

        radar = go.Figure()
        radar.add_trace(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill="toself",
                fillcolor=f"{color}2a",
                line=dict(color=color, width=2.5),
                marker=dict(size=7, color=color),
                name="Score",
            )
        )
        radar.update_layout(
            polar=dict(
                bgcolor="#111",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10),
                    gridcolor="#333",
                ),
                angularaxis=dict(gridcolor="#333"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            height=380,
            margin=dict(l=50, r=50, t=30, b=30),
        )
        st.plotly_chart(radar, use_container_width=True)

    with right:
        st.subheader("Google Trends — Last 12 Months")
        trend_df: pd.DataFrame = trends_result.get("data", pd.DataFrame())

        if not trend_df.empty:
            col_name = trend_df.columns[0]
            line = go.Figure()
            line.add_trace(
                go.Scatter(
                    x=trend_df.index,
                    y=trend_df[col_name],
                    mode="lines",
                    line=dict(color=color, width=2.5),
                    fill="tozeroy",
                    fillcolor=f"{color}22",
                    name=keyword,
                )
            )
            line.update_layout(
                xaxis_title="Date",
                yaxis_title="Interest (0 – 100)",
                yaxis=dict(range=[0, 105], gridcolor="#333"),
                xaxis=dict(gridcolor="#333"),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=380,
                margin=dict(l=50, r=20, t=30, b=50),
                hovermode="x unified",
            )
            st.plotly_chart(line, use_container_width=True)
        else:
            st.info(
                "No Google Trends data returned for this keyword. "
                "Try a broader term or check for rate-limiting."
            )
            if "error" in trends_result:
                st.caption(f"Error: {trends_result['error']}")

    st.divider()

    # ── Raw data metrics ──────────────────────────────────────────────────────
    st.subheader("Raw Signal Data")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Trend Score", f"{scores['trend_score']} / 100")
    m2.metric("Buzz Score", f"{scores['buzz_score']} / 100")
    m3.metric("Sales Potential Score", f"{scores['sales_score']} / 100")
    m4.metric("Est. Monthly Sales", f"{est_sales:,.0f} units")

    with st.expander("Signal details"):
        detail_col1, detail_col2, detail_col3 = st.columns(3)
        detail_col1.markdown(
            f"**Avg. Google Trends interest:** {trends_result['average']:.1f} / 100"
        )
        detail_col2.markdown(
            f"**Reddit mentions (30 days):** {reddit_result['mentions']}"
        )
        detail_col3.markdown(
            f"**BSR entered:** {bsr:,}  \n**Formula:** 3000 ÷ {bsr}^0.7 = {est_sales:,.1f}"
        )

        if "error" in reddit_result:
            st.caption(f"Reddit fetch issue: {reddit_result['error']}")
        if "error" in trends_result:
            st.caption(f"Trends fetch issue: {trends_result['error']}")
