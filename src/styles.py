from __future__ import annotations


def app_css(dark_mode: bool) -> str:
    if dark_mode:
        bg = "#070b16"
        panel = "#101827"
        panel_2 = "#152033"
        text = "#f8fafc"
        muted = "#94a3b8"
        border = "rgba(148, 163, 184, 0.20)"
        accent = "#f97316"
        accent_2 = "#22c55e"
        shadow = "0 18px 50px rgba(0, 0, 0, 0.35)"
    else:
        bg = "#f7f8fb"
        panel = "#ffffff"
        panel_2 = "#eef2f7"
        text = "#0f172a"
        muted = "#64748b"
        border = "rgba(15, 23, 42, 0.12)"
        accent = "#ea580c"
        accent_2 = "#0891b2"
        shadow = "0 16px 40px rgba(15, 23, 42, 0.10)"

    return f"""
    <style>
    :root {{
        --riq-bg: {bg};
        --riq-panel: {panel};
        --riq-panel-2: {panel_2};
        --riq-text: {text};
        --riq-muted: {muted};
        --riq-border: {border};
        --riq-accent: {accent};
        --riq-accent-2: {accent_2};
        --riq-shadow: {shadow};
    }}

    .stApp {{
        background:
            radial-gradient(circle at 12% 8%, rgba(249, 115, 22, 0.18), transparent 28%),
            radial-gradient(circle at 88% 14%, rgba(34, 197, 94, 0.12), transparent 22%),
            var(--riq-bg);
        color: var(--riq-text);
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        max-width: 1440px;
        padding-top: 1.3rem;
        padding-bottom: 2rem;
    }}

    .topbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        padding: 18px 20px;
        border: 1px solid var(--riq-border);
        border-radius: 8px;
        background: color-mix(in srgb, var(--riq-panel) 92%, transparent);
        box-shadow: var(--riq-shadow);
        margin-bottom: 18px;
    }}

    .brand-lockup {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}

    .logo-mark {{
        width: 44px;
        height: 44px;
        display: grid;
        place-items: center;
        border-radius: 8px;
        background: linear-gradient(135deg, var(--riq-accent), #ef4444);
        color: white;
        font-weight: 900;
        letter-spacing: 0;
    }}

    .eyebrow {{
        color: var(--riq-muted);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0;
    }}

    .app-title {{
        color: var(--riq-text);
        font-size: clamp(1.6rem, 2.4vw, 2.6rem);
        font-weight: 850;
        line-height: 1.05;
        margin: 0;
        letter-spacing: 0;
    }}

    .hero-grid {{
        display: grid;
        grid-template-columns: 1.28fr 0.72fr;
        gap: 16px;
        margin-bottom: 18px;
    }}

    .hero-panel,
    .insight-panel,
    .metric-card,
    .chart-shell {{
        border: 1px solid var(--riq-border);
        background: color-mix(in srgb, var(--riq-panel) 94%, transparent);
        border-radius: 8px;
        box-shadow: var(--riq-shadow);
    }}

    .hero-panel {{
        padding: 24px;
        min-height: 230px;
        position: relative;
        overflow: hidden;
    }}

    .hero-panel:after {{
        content: "";
        position: absolute;
        inset: auto 18px 18px auto;
        width: 210px;
        height: 126px;
        border-radius: 8px;
        background:
            linear-gradient(90deg, transparent 0 18%, rgba(249, 115, 22, 0.65) 18% 24%, transparent 24% 38%, rgba(34, 197, 94, 0.58) 38% 44%, transparent 44% 60%, rgba(14, 165, 233, 0.62) 60% 66%, transparent 66%),
            linear-gradient(180deg, rgba(148, 163, 184, 0.12), rgba(148, 163, 184, 0.02));
        opacity: 0.9;
    }}

    .hero-copy {{
        max-width: 760px;
        color: var(--riq-muted);
        font-size: 1.02rem;
        line-height: 1.65;
        margin-top: 14px;
    }}

    .insight-panel {{
        padding: 20px;
    }}

    .insight-label {{
        color: var(--riq-muted);
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 12px;
    }}

    .insight-number {{
        font-size: 2.2rem;
        font-weight: 900;
        color: var(--riq-text);
        line-height: 1.0;
    }}

    .insight-text {{
        color: var(--riq-muted);
        line-height: 1.55;
        margin-top: 12px;
    }}

    .metric-card {{
        padding: 15px;
        min-height: 118px;
    }}

    .metric-label {{
        color: var(--riq-muted);
        font-size: 0.82rem;
        margin-bottom: 10px;
    }}

    .metric-value {{
        color: var(--riq-text);
        font-size: 1.55rem;
        line-height: 1.1;
        font-weight: 850;
        overflow-wrap: anywhere;
    }}

    .metric-delta {{
        color: var(--riq-accent-2);
        font-size: 0.82rem;
        margin-top: 10px;
    }}

    .section-title {{
        color: var(--riq-text);
        font-size: 1.2rem;
        font-weight: 820;
        margin: 10px 0 4px;
    }}

    .section-note {{
        color: var(--riq-muted);
        margin: 0 0 12px;
        line-height: 1.55;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        background: var(--riq-panel);
        border: 1px solid var(--riq-border);
        border-radius: 8px;
        padding: 6px;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 7px;
        padding: 10px 13px;
        color: var(--riq-muted);
        font-weight: 700;
        letter-spacing: 0;
    }}

    .stTabs [aria-selected="true"] {{
        background: var(--riq-panel-2);
        color: var(--riq-text);
    }}

    div[data-testid="stMetric"] {{
        border: 1px solid var(--riq-border);
        background: var(--riq-panel);
        border-radius: 8px;
        padding: 13px;
    }}

    [data-testid="stSidebar"] {{
        background: color-mix(in srgb, var(--riq-panel) 96%, var(--riq-bg));
        border-right: 1px solid var(--riq-border);
    }}

    .stDataFrame {{
        border: 1px solid var(--riq-border);
        border-radius: 8px;
        overflow: hidden;
    }}

    @media (max-width: 900px) {{
        .topbar,
        .hero-grid {{
            grid-template-columns: 1fr;
            display: grid;
        }}
        .topbar {{
            align-items: start;
        }}
        .hero-panel:after {{
            opacity: 0.28;
        }}
    }}
    </style>
    """


def metric_card(label: str, value: str, delta: str = "") -> str:
    return f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-delta">{delta}</div>
    </div>
    """

