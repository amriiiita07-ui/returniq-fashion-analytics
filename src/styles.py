"""
ReturnIQ – Styles
=================
WHAT CHANGED
------------
1. Legend overlap fix  → All chart margin/legend settings are now in styles.py
   as a shared helper `fix_legend(fig)` so every chart gets the same treatment.
2. Completely new colour palette  → "Volcanic Ember" dark theme.
   Deep obsidian backgrounds, molten amber/coral accents, electric teal highlights.
3. Plotly layout defaults baked in via `apply_theme(fig, dark)` so every chart
   is consistent without touching individual chart files.
"""

from __future__ import annotations

# ── Palette ──────────────────────────────────────────────────────────────────
# "Volcanic Ember" — obsidian depths, molten amber, electric teal, coral pulse
DARK = {
    "bg":          "#0D0E12",   # obsidian canvas
    "surface":     "#14161E",   # card/panel
    "surface2":    "#1C1F2B",   # raised element
    "border":      "#2A2D3E",   # subtle border
    "text":        "#E8E6E0",   # warm white
    "muted":       "#7A7A90",   # secondary text
    "accent1":     "#FF6B35",   # molten orange (primary accent)
    "accent2":     "#00D4B1",   # electric teal (secondary accent)
    "accent3":     "#FF3F74",   # coral pulse (alerts / loss)
    "accent4":     "#FFBC3B",   # amber glow (revenue)
    "accent5":     "#8B5CF6",   # violet haze (cohort)
    "accent6":     "#34D399",   # emerald success
    "grid":        "#1E2030",   # chart grid
    "plot_bg":     "#0D0E12",
}

LIGHT = {
    "bg":          "#F5F2ED",
    "surface":     "#FFFFFF",
    "surface2":    "#EDEBE5",
    "border":      "#D4D0C8",
    "text":        "#1A1814",
    "muted":       "#6B6860",
    "accent1":     "#E05520",
    "accent2":     "#009E85",
    "accent3":     "#D42054",
    "accent4":     "#C8860A",
    "accent5":     "#6D28D9",
    "accent6":     "#059669",
    "grid":        "#E8E4DC",
    "plot_bg":     "#F5F2ED",
}

# Ordered category palette (for line/bar/donut series)
CATEGORY_COLORS_DARK = [
    "#FF6B35",  # Accessories  – molten orange
    "#00D4B1",  # Activewear   – electric teal
    "#FFBC3B",  # Beauty        – amber glow
    "#FF3F74",  # Ethnic Wear  – coral pulse
    "#8B5CF6",  # Footwear     – violet haze
    "#34D399",  # Western Wear – emerald
]

CATEGORY_COLORS_LIGHT = [
    "#E05520",
    "#009E85",
    "#C8860A",
    "#D42054",
    "#6D28D9",
    "#059669",
]


def palette(dark: bool) -> dict:
    return DARK if dark else LIGHT


def cat_colors(dark: bool) -> list[str]:
    return CATEGORY_COLORS_DARK if dark else CATEGORY_COLORS_LIGHT


# ── Plotly helpers ────────────────────────────────────────────────────────────

def fix_legend(fig):
    """
    Push legend BELOW the chart so it never overlaps titles.
    Call this on every figure before st.plotly_chart().
    """
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,          # well below the plot area
            xanchor="center",
            x=0.5,
            font=dict(size=11),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
        margin=dict(t=56, b=96, l=48, r=24),
    )
    return fig


def apply_theme(fig, dark: bool):
    """Apply the Volcanic Ember theme to any plotly figure."""
    p = palette(dark)
    fig.update_layout(
        paper_bgcolor=p["surface"],
        plot_bgcolor=p["plot_bg"],
        font=dict(
            family="'IBM Plex Sans', 'Inter', sans-serif",
            color=p["text"],
            size=12,
        ),
        title_font=dict(size=14, color=p["text"], family="'IBM Plex Mono', monospace"),
        xaxis=dict(
            gridcolor=p["grid"],
            linecolor=p["border"],
            tickcolor=p["border"],
            tickfont=dict(color=p["muted"], size=11),
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor=p["grid"],
            linecolor=p["border"],
            tickcolor=p["border"],
            tickfont=dict(color=p["muted"], size=11),
            zeroline=False,
        ),
        colorway=cat_colors(dark),
        hoverlabel=dict(
            bgcolor=p["surface2"],
            bordercolor=p["border"],
            font=dict(color=p["text"], size=12),
        ),
    )
    return fix_legend(fig)


# ── CSS ───────────────────────────────────────────────────────────────────────

def app_css(dark: bool) -> str:
    p = palette(dark)

    return f"""
<style>
/* ── Google Fonts ──────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

/* ── Reset / globals ───────────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; }}

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main .block-container {{
    background-color: {p["bg"]} !important;
    color: {p["text"]} !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}}

/* ── Sidebar ────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: {p["surface"]} !important;
    border-right: 1px solid {p["border"]} !important;
}}
[data-testid="stSidebar"] * {{
    color: {p["text"]} !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}}

/* ── Topbar ─────────────────────────────────────────────── */
.topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 28px 18px;
    background: linear-gradient(135deg, {p["surface"]} 0%, {p["surface2"]} 100%);
    border: 1px solid {p["border"]};
    border-radius: 16px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}}
.topbar::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, {p["accent1"]}, {p["accent2"]}, {p["accent5"]});
}}
.brand-lockup {{
    display: flex;
    align-items: center;
    gap: 16px;
}}
.logo-mark {{
    width: 48px; height: 48px;
    border-radius: 12px;
    background: linear-gradient(135deg, {p["accent1"]} 0%, {p["accent3"]} 100%);
    display: flex; align-items: center; justify-content: center;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600; font-size: 14px;
    color: #fff;
    letter-spacing: -0.5px;
    flex-shrink: 0;
    box-shadow: 0 4px 16px {p["accent1"]}44;
}}
.eyebrow {{
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: {p["muted"]};
    margin: 0 0 2px;
}}
.app-title {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 20px;
    font-weight: 600;
    color: {p["text"]};
    margin: 0;
    letter-spacing: -0.5px;
    line-height: 1.2;
}}

/* ── Hero grid ──────────────────────────────────────────── */
.hero-grid {{
    display: grid;
    grid-template-columns: 1fr 320px;
    gap: 16px;
    margin: 16px 0 20px;
}}
.hero-panel {{
    background: {p["surface"]};
    border: 1px solid {p["border"]};
    border-radius: 14px;
    padding: 24px 28px;
}}
.hero-copy {{
    font-size: 13px;
    color: {p["muted"]};
    line-height: 1.65;
    margin: 8px 0 0;
}}
.insight-panel {{
    background: linear-gradient(145deg, {p["surface2"]} 0%, {p["surface"]} 100%);
    border: 1px solid {p["accent1"]}55;
    border-radius: 14px;
    padding: 24px 28px;
    position: relative;
    overflow: hidden;
}}
.insight-panel::after {{
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 100px; height: 100px;
    border-radius: 50%;
    background: {p["accent1"]}18;
}}
.insight-label {{
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: {p["accent1"]};
    margin-bottom: 6px;
}}
.insight-number {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 52px;
    font-weight: 600;
    color: {p["accent1"]};
    line-height: 1;
    margin-bottom: 8px;
    letter-spacing: -2px;
}}
.insight-text {{
    font-size: 12px;
    color: {p["muted"]};
    line-height: 1.55;
}}
.insight-text strong {{
    color: {p["accent4"]};
}}

/* ── Metric cards ───────────────────────────────────────── */
.metric-card {{
    background: {p["surface"]};
    border: 1px solid {p["border"]};
    border-radius: 12px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease;
}}
.metric-card:hover {{
    border-color: {p["accent2"]}66;
}}
.metric-card::before {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, {p["accent2"]}80, {p["accent1"]}80);
    opacity: 0.6;
}}
.metric-label {{
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: {p["muted"]};
    margin: 0 0 6px;
}}
.metric-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 22px;
    font-weight: 600;
    color: {p["text"]};
    letter-spacing: -0.5px;
    margin: 0 0 4px;
}}
.metric-delta {{
    font-size: 10px;
    color: {p["muted"]};
    margin: 0;
}}

/* ── Section headings ───────────────────────────────────── */
.section-title {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: {p["accent2"]};
    margin-bottom: 2px;
    padding-bottom: 8px;
    border-bottom: 1px solid {p["border"]};
}}
.section-note {{
    font-size: 12px;
    color: {p["muted"]};
    margin: 4px 0 16px;
}}

/* ── Tabs ───────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {{
    border-bottom: 1px solid {p["border"]} !important;
    gap: 2px !important;
}}
[data-testid="stTabs"] button[role="tab"] {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    color: {p["muted"]} !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 8px 14px !important;
    border: none !important;
    background: transparent !important;
    transition: color 0.2s, background 0.2s !important;
}}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
    color: {p["accent2"]} !important;
    background: {p["surface2"]} !important;
    border-bottom: 2px solid {p["accent2"]} !important;
}}
[data-testid="stTabs"] button[role="tab"]:hover:not([aria-selected="true"]) {{
    color: {p["text"]} !important;
    background: {p["surface"]} !important;
}}

/* ── Dataframe / table ──────────────────────────────────── */
[data-testid="stDataFrame"] {{
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid {p["border"]} !important;
}}

/* ── Scrollbar ──────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {p["bg"]}; }}
::-webkit-scrollbar-thumb {{ background: {p["border"]}; border-radius: 2px; }}

/* ── Download buttons ───────────────────────────────────── */
[data-testid="stDownloadButton"] > button {{
    background: {p["surface2"]} !important;
    color: {p["text"]} !important;
    border: 1px solid {p["border"]} !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    transition: border-color 0.2s !important;
}}
[data-testid="stDownloadButton"] > button:hover {{
    border-color: {p["accent2"]} !important;
    color: {p["accent2"]} !important;
}}
</style>
"""


def metric_card(label: str, value: str, delta: str = "") -> str:
    return f"""
<div class="metric-card">
  <p class="metric-label">{label}</p>
  <p class="metric-value">{value}</p>
  {"<p class='metric-delta'>" + delta + "</p>" if delta else ""}
</div>
"""
