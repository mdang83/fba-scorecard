import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from data.fetcher import fetch_google_trends, fetch_reddit_mentions, estimate_monthly_sales
from scorer import calculate_opportunity_score
import styles

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FBA Opportunity Scorecard",
    page_icon="📦",
    layout="wide",
)
styles.inject_css()

# ── Plotly builders ───────────────────────────────────────────────────────────

def _gauge(score: float, color: str) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            "font": {
                "size": 58,
                "color": color,
                "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            },
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickvals": [0, 25, 50, 75, 100],
                "tickfont": {"color": styles.TEXT_MUT, "size": 9},
                "tickwidth": 1,
                "tickcolor": styles.BORDER,
            },
            "bar": {"color": color, "thickness": 0.2},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "bordercolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0,  40], "color": "rgba(239,68,68,0.10)"},
                {"range": [40, 70], "color": "rgba(245,158,11,0.10)"},
                {"range": [70,100], "color": "rgba(16,185,129,0.10)"},
            ],
            "threshold": {
                "line": {"color": color, "width": 4},
                "thickness": 0.78,
                "value": score,
            },
        },
        title={
            "text": "OPPORTUNITY SCORE",
            "font": {"size": 10, "color": styles.TEXT_MUT},
            "align": "center",
        },
        domain={"x": [0, 1], "y": [0.05, 1]},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=290,
        margin={"l": 25, "r": 25, "t": 45, "b": 5},
        font={"color": styles.TEXT_SEC, "family": "-apple-system, sans-serif"},
    )
    return fig


def _sparkline(df: pd.DataFrame, keyword: str) -> go.Figure | None:
    if df is None or df.empty:
        return None
    try:
        col = df.columns[0]
        x = list(df.index)
        y = [float(v) for v in df[col]]
    except Exception:
        return None

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        line=dict(color=styles.ACCENT, width=2),
        fill="tozeroy",
        fillcolor="rgba(99,102,241,0.07)",
        hovertemplate="%{x|%b %Y}  ·  interest: %{y:.0f}<extra></extra>",
        name=keyword,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=170,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            tickfont=dict(color=styles.TEXT_MUT, size=9),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(42,63,95,0.35)",
            showline=False,
            zeroline=False,
            tickfont=dict(color=styles.TEXT_MUT, size=9),
            range=[0, 108],
            title=None,
        ),
        hovermode="x unified",
        showlegend=False,
    )
    return fig


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="font-size:0.62rem;font-weight:700;letter-spacing:0.16em;'
        'text-transform:uppercase;color:#6366f1;margin-bottom:1.25rem;">How it works</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "1. Enter a **product keyword** — e.g. *bamboo cutting board*  \n"
        "2. Enter the **BSR** from a competitor's listing  \n"
        "3. Click **Analyze**"
    )
    st.divider()
    st.markdown(
        '<div style="font-size:0.62rem;font-weight:700;letter-spacing:0.16em;'
        'text-transform:uppercase;color:#6366f1;margin-bottom:0.75rem;">Score guide</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "| Score | Signal |\n|---|---|\n"
        "| ≥ 70 | 🟢 Strong |\n"
        "| 40 – 69 | 🟡 Moderate |\n"
        "| < 40 | 🔴 Weak |"
    )
    st.divider()
    st.markdown(
        '<div style="font-size:0.62rem;font-weight:700;letter-spacing:0.16em;'
        'text-transform:uppercase;color:#6366f1;margin-bottom:0.75rem;">Reddit setup</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "Add credentials to `.streamlit/secrets.toml`:\n"
        "```toml\n[reddit]\nclient_id = \"…\"\nclient_secret = \"…\"\n"
        "user_agent = \"fba-scorecard/1.0\"\n```\n"
        "Without them the Buzz Score defaults to 0."
    )
    st.divider()
    st.markdown(
        '<div style="font-size:0.62rem;font-weight:700;letter-spacing:0.16em;'
        'text-transform:uppercase;color:#6366f1;margin-bottom:0.75rem;">Signal weights</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "- **Trend** (40%) — Google search interest  \n"
        "- **Buzz** (30%) — Reddit post volume  \n"
        "- **Sales** (30%) — BSR-derived estimate"
    )

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(styles.hero(), unsafe_allow_html=True)

# ── Input strip ───────────────────────────────────────────────────────────────
col_kw, col_bsr, col_btn = st.columns([3.5, 2, 1.2])
with col_kw:
    keyword = st.text_input(
        "Product Keyword",
        placeholder="e.g. bamboo cutting board",
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
    analyze = st.button("Analyze", type="primary", use_container_width=True)

# ── Analysis ──────────────────────────────────────────────────────────────────
if not analyze:
    st.markdown(styles.empty_state(), unsafe_allow_html=True)
    st.stop()

if not keyword.strip():
    st.error("Enter a product keyword to continue.")
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
        "Reddit credentials not configured — Buzz Score will be 0. "
        "See sidebar for setup instructions.",
        icon="ℹ️",
    )

try:
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

    opp  = scores["opportunity_score"]
    c    = styles.score_color(opp)

    # ── Score centerpiece ─────────────────────────────────────────────────────
    gauge_col, cards_col = st.columns([5, 7], gap="large")

    with gauge_col:
        st.plotly_chart(_gauge(opp, c), use_container_width=True, config={"displayModeBar": False})
        st.markdown(styles.verdict(opp), unsafe_allow_html=True)

    with cards_col:
        trend_s = scores["trend_score"]
        buzz_s  = scores["buzz_score"]
        sales_s = scores["sales_score"]

        cards_html = (
            '<div class="metric-grid">'
            + styles.metric_card(
                "Est. Monthly Sales",
                f"{est_sales:,.0f}",
                "units / month",
                0,
                "",
                show_bar=False,
            )
            + styles.metric_card(
                "Trend Score",
                f"{trend_s:.0f}",
                "out of 100 · google trends",
                trend_s,
                styles.score_color(trend_s),
            )
            + styles.metric_card(
                "Buzz Score",
                f"{buzz_s:.0f}",
                "out of 100 · reddit signal",
                buzz_s,
                styles.score_color(buzz_s),
            )
            + styles.metric_card(
                "Sales Score",
                f"{sales_s:.0f}",
                "out of 100 · bsr-derived",
                sales_s,
                styles.score_color(sales_s),
            )
            + "</div>"
        )
        st.markdown(cards_html, unsafe_allow_html=True)

    # ── Google Trends sparkline ────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    trend_df: pd.DataFrame = trends_result.get("data", pd.DataFrame())
    fig_spark = _sparkline(trend_df, keyword.strip())

    st.markdown(
        styles.section_card(
            "Google Trends",
            f'"{keyword.strip()}" · last 12 months · interest 0–100',
        ),
        unsafe_allow_html=True,
    )

    if fig_spark:
        st.plotly_chart(fig_spark, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown(
            '<div style="padding:2rem 0;text-align:center;color:#64748b;font-size:0.82rem;">'
            "No trend data returned for this keyword — try a broader term.</div>",
            unsafe_allow_html=True,
        )
        if "error" in trends_result:
            st.caption(f"Fetch error: {trends_result['error']}")

    # ── Raw signal data ────────────────────────────────────────────────────────
    with st.expander("Raw signal data"):
        st.markdown(
            styles.raw_data(
                trends_result["average"],
                reddit_result["mentions"],
                bsr,
                est_sales,
            ),
            unsafe_allow_html=True,
        )
        if "error" in reddit_result:
            st.caption(f"Reddit: {reddit_result['error']}")
        if "error" in trends_result:
            st.caption(f"Trends: {trends_result['error']}")

except Exception as exc:
    st.error(
        f"Something went wrong while analyzing **{keyword.strip()}** — {exc}. "
        "Try adjusting your inputs and running the analysis again.",
        icon="⚠️",
    )
