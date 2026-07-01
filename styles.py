"""
Design system for the FBA Opportunity Scorecard.
Import inject_css() and the HTML helpers into app.py.
Color constants are also exported for use in Plotly figures.
"""

import streamlit as st

# ── Color tokens ──────────────────────────────────────────────────────────────
NAVY_900   = "#0a1628"
NAVY_800   = "#0d1b2a"
NAVY_700   = "#132236"
NAVY_600   = "#1a2940"
BORDER     = "#2a3f5f"
BORDER_SUB = "#1e3148"

TEXT_PRI  = "#e2e8f0"
TEXT_SEC  = "#94a3b8"
TEXT_MUT  = "#64748b"

ACCENT         = "#6366f1"   # indigo — UI chrome, sparkline
SCORE_STRONG   = "#10b981"   # emerald  ≥70
SCORE_MODERATE = "#f59e0b"   # amber    40–69
SCORE_WEAK     = "#ef4444"   # red      <40


def score_color(score: float) -> str:
    if score >= 70:
        return SCORE_STRONG
    if score >= 40:
        return SCORE_MODERATE
    return SCORE_WEAK


def score_label(score: float) -> str:
    if score >= 70:
        return "Strong Opportunity"
    if score >= 40:
        return "Moderate Opportunity"
    return "Weak Opportunity"


# ── CSS ───────────────────────────────────────────────────────────────────────
_CSS = """
<style>
/* ── Reset ─────────────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                 "Segoe UI", system-ui, sans-serif;
    color: #e2e8f0;
}
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: #0a1628; }

.block-container {
    max-width: 1080px !important;
    padding: 0 2rem 5rem !important;
    margin: 0 auto !important;
}

/* ── Sidebar ────────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #0d1b2a !important;
    border-right: 1px solid #1e3148 !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 2rem 1.5rem !important;
}
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] span {
    color: #94a3b8 !important;
}
section[data-testid="stSidebar"] strong,
section[data-testid="stSidebar"] b { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] th { color: #64748b !important; font-size: 0.7rem !important; }
section[data-testid="stSidebar"] td { color: #94a3b8 !important; font-size: 0.8rem !important; }
section[data-testid="stSidebar"] table {
    border-collapse: collapse;
    width: 100%;
}
section[data-testid="stSidebar"] tr {
    border-bottom: 1px solid #1e3148 !important;
}
section[data-testid="stSidebar"] hr {
    border-top: 1px solid #1e3148 !important;
}
section[data-testid="stSidebar"] code {
    background: #132236 !important;
    color: #94a3b8 !important;
    border: 1px solid #2a3f5f !important;
    font-size: 0.72rem !important;
}

/* ── Inputs ─────────────────────────────────────────────────────────────────── */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background: #132236 !important;
    border: 1px solid #2a3f5f !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-size: 0.9rem !important;
    box-shadow: none !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label {
    color: #64748b !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stNumberInput"] input::placeholder {
    color: #2a3f5f !important;
}
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background: #1a2940 !important;
    border: 1px solid #2a3f5f !important;
    color: #64748b !important;
    border-radius: 4px !important;
}

/* ── Primary button ─────────────────────────────────────────────────────────── */
button[data-testid="baseButton-primary"] {
    background: #6366f1 !important;
    border: none !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 2px 12px rgba(99,102,241,0.35) !important;
    transition: background 0.15s, box-shadow 0.15s, transform 0.08s !important;
}
button[data-testid="baseButton-primary"]:hover {
    background: #4f46e5 !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.45) !important;
}
button[data-testid="baseButton-primary"]:active { transform: scale(0.97) !important; }

/* ── Expander ───────────────────────────────────────────────────────────────── */
div[data-testid="stExpander"] {
    background: #132236 !important;
    border: 1px solid #1e3148 !important;
    border-radius: 10px !important;
}
div[data-testid="stExpander"] summary {
    color: #64748b !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
div[data-testid="stExpander"] summary:hover { color: #94a3b8 !important; }

/* ── Alerts / warnings ──────────────────────────────────────────────────────── */
div[data-testid="stAlert"] {
    background: #132236 !important;
    border: 1px solid #2a3f5f !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
}

/* ── Spinner ────────────────────────────────────────────────────────────────── */
div[data-testid="stSpinner"] > div { border-top-color: #6366f1 !important; }

/* ── Dividers ───────────────────────────────────────────────────────────────── */
hr { border: none !important; border-top: 1px solid #1e3148 !important; margin: 2rem 0 !important; }

/* ── Hero ───────────────────────────────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #0d1b2a 0%, #132236 100%);
    border-bottom: 1px solid #1e3148;
    padding: 2.75rem 0 2.25rem;
    margin: 0 -2rem 2.25rem;
}
.hero-inner { max-width: 1080px; margin: 0 auto; padding: 0 2rem; }
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #6366f1;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.22);
    border-radius: 4px;
    padding: 3px 10px;
    margin-bottom: 0.9rem;
}
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff !important;
    letter-spacing: -0.03em;
    line-height: 1.12;
    margin: 0 0 0.55rem;
}
.hero-sub {
    font-size: 0.9rem;
    color: #64748b;
    font-weight: 400;
    line-height: 1.65;
    max-width: 540px;
    margin: 0;
}

/* ── Input strip ────────────────────────────────────────────────────────────── */
.input-strip {
    background: #132236;
    border: 1px solid #1e3148;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 2rem;
}

/* ── Score verdict ──────────────────────────────────────────────────────────── */
.verdict-wrap { text-align: center; margin-top: -6px; margin-bottom: 0.5rem; }
.verdict-badge {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    border-radius: 6px;
    padding: 4px 14px;
}

/* ── Metric cards ───────────────────────────────────────────────────────────── */
.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.65rem;
}
.mcard {
    background: #132236;
    border: 1px solid #1e3148;
    border-radius: 10px;
    padding: 1rem 1.15rem;
    display: flex;
    flex-direction: column;
    gap: 0;
}
.mcard-label {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.35rem;
}
.mcard-value {
    font-size: 1.55rem;
    font-weight: 700;
    color: #e2e8f0;
    line-height: 1;
    margin-bottom: 0.18rem;
    font-variant-numeric: tabular-nums;
}
.mcard-unit {
    font-size: 0.68rem;
    color: #64748b;
    margin-bottom: 0.65rem;
}
.mbar { height: 3px; background: #2a3f5f; border-radius: 2px; overflow: hidden; }
.mbar-fill { height: 100%; border-radius: 2px; }

/* ── Section card ───────────────────────────────────────────────────────────── */
.scard {
    background: #132236;
    border: 1px solid #1e3148;
    border-radius: 12px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 0.85rem;
}
.scard-head {
    display: flex;
    align-items: baseline;
    gap: 0.7rem;
    margin-bottom: 1.1rem;
}
.scard-title {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #64748b;
}
.scard-sub { font-size: 0.82rem; color: #94a3b8; font-weight: 400; }

/* ── Raw data ───────────────────────────────────────────────────────────────── */
.raw-row { display: flex; gap: 2.5rem; flex-wrap: wrap; }
.raw-item { display: flex; flex-direction: column; gap: 3px; }
.raw-lbl {
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748b;
}
.raw-val { font-size: 0.88rem; font-weight: 500; color: #94a3b8; font-variant-numeric: tabular-nums; }

/* ── Empty state ────────────────────────────────────────────────────────────── */
.empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5.5rem 2rem;
    text-align: center;
}
.empty-icon {
    width: 52px; height: 52px;
    border-radius: 13px;
    background: #132236;
    border: 1px solid #2a3f5f;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 1.1rem;
}
.empty-title { font-size: 0.95rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.35rem; }
.empty-body  { font-size: 0.82rem; color: #64748b; max-width: 360px; line-height: 1.65; }

/* ── Sidebar code block — prevent horizontal clipping ────────────────────── */
[data-testid="stSidebar"] pre,
[data-testid="stSidebar"] code {
    white-space: pre-wrap !important;
    word-break: break-word !important;
    overflow-wrap: break-word !important;
    overflow-x: hidden !important;
    font-size: 0.72rem !important;
}

/* ── Responsive ─────────────────────────────────────────────────────────────── */
@media (max-width: 760px) {
    .hero-title { font-size: 1.5rem; }
    .metric-grid { grid-template-columns: 1fr 1fr; }
    .raw-row { gap: 1.25rem; }
    .mcard-value { font-size: 1.3rem; }
}
@media (max-width: 480px) {
    .hero-title { font-size: 1.2rem; }
    .hero-sub { font-size: 0.8rem; }
    .metric-grid {
        grid-template-columns: 1fr !important;
    }
    .mcard-value { font-size: 1.15rem; }
    .mcard { padding: 0.75rem 0.9rem; }
    .scard { padding: 0.9rem 1rem; }
}
</style>
"""


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


# ── HTML component builders ───────────────────────────────────────────────────

def hero() -> str:
    return """
    <div class="hero">
      <div class="hero-inner">
        <div class="hero-eyebrow">Amazon FBA Research Tool</div>
        <h1 class="hero-title">FBA Opportunity Scorecard</h1>
        <p class="hero-sub">Score any product niche in seconds — live Google Trends data,
        Reddit community buzz, and BSR-derived sales estimates combined into one
        composite opportunity signal.</p>
      </div>
    </div>
    """


def verdict(score: float) -> str:
    c = score_color(score)
    lbl = score_label(score)
    return (
        f'<div class="verdict-wrap">'
        f'<span class="verdict-badge" '
        f'style="color:{c};background:{c}18;border:1px solid {c}33;">'
        f'{lbl}'
        f'</span></div>'
    )


def metric_card(
    label: str, value: str, unit: str, pct: float, color: str, show_bar: bool = True
) -> str:
    if show_bar:
        pct = max(0.0, min(100.0, pct))
        bar = (
            f'<div class="mbar"><div class="mbar-fill" '
            f'style="width:{pct:.1f}%;background:{color};"></div></div>'
        )
    else:
        bar = ""
    return (
        f'<div class="mcard">'
        f'<div class="mcard-label">{label}</div>'
        f'<div class="mcard-value">{value}</div>'
        f'<div class="mcard-unit">{unit}</div>'
        f'{bar}'
        f'</div>'
    )


def section_card(title: str, subtitle: str = "") -> str:
    sub = f'<span class="scard-sub">{subtitle}</span>' if subtitle else ""
    return (
        f'<div class="scard">'
        f'<div class="scard-head"><span class="scard-title">{title}</span>{sub}</div>'
    )


def raw_data(trend_avg: float, mentions: int, bsr: int, est_sales: float) -> str:
    items = [
        ("Avg Trend Interest",   f"{trend_avg:.1f} / 100"),
        ("Reddit Mentions (30d)", str(mentions)),
        ("Best Seller Rank",      f"{bsr:,}"),
        ("Est Monthly Sales",     f"{est_sales:,.0f} units"),
    ]
    inner = "".join(
        f'<div class="raw-item">'
        f'<span class="raw-lbl">{lbl}</span>'
        f'<span class="raw-val">{val}</span>'
        f'</div>'
        for lbl, val in items
    )
    return f'<div class="raw-row">{inner}</div>'


def empty_state() -> str:
    return (
        '<div class="empty">'
        '<div class="empty-icon">📊</div>'
        '<div class="empty-title">No analysis yet</div>'
        '<div class="empty-body">Enter a product keyword and Best Seller Rank above, '
        'then click Analyze to generate your opportunity scorecard.</div>'
        '</div>'
    )
