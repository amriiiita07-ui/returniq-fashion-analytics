"""
ReturnIQ – Charts
=================
KEY CHANGE: Every figure now calls `apply_theme(fig, dark)` from styles.py.
`apply_theme` calls `fix_legend` internally, so legends are ALWAYS below the
plot area and never overlap titles.

Individual chart functions no longer set legend/margin manually.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.styles import apply_theme, cat_colors, palette


# ── helpers ───────────────────────────────────────────────────────────────────

def _themed(fig, dark: bool) -> go.Figure:
    """Convenience: apply theme + fix legend in one call."""
    return apply_theme(fig, dark)


# ── 1. Monthly profit line ────────────────────────────────────────────────────

def monthly_profit_line(monthly: pd.DataFrame, dark: bool) -> go.Figure:
    p = palette(dark)
    colors = cat_colors(dark)
    fig = go.Figure()
    for i, cat in enumerate(monthly["category"].unique()):
        df = monthly[monthly["category"] == cat].sort_values("month")
        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=df["month"],
            y=df["return_adjusted_profit"],
            name=cat,
            mode="lines+markers",
            line=dict(color=color, width=2.5, shape="spline"),
            marker=dict(size=6, color=color, line=dict(width=1.5, color=p["surface"])),
            hovertemplate=f"<b>{cat}</b><br>Month: %{{x}}<br>Profit: ₹%{{y:,.0f}}<extra></extra>",
        ))
    fig.update_layout(title=dict(text="Return-adjusted profit by month", x=0))
    return _themed(fig, dark)


# ── 2. Category donut ─────────────────────────────────────────────────────────

def category_donut(monthly: pd.DataFrame, dark: bool) -> go.Figure:
    p = palette(dark)
    agg = monthly.groupby("category", as_index=False)["return_adjusted_profit"].sum()
    colors = cat_colors(dark)
    fig = go.Figure(go.Pie(
        labels=agg["category"],
        values=agg["return_adjusted_profit"],
        hole=0.62,
        marker=dict(colors=colors[:len(agg)], line=dict(color=p["surface"], width=2)),
        textinfo="percent",
        textfont=dict(size=11),
        hovertemplate="<b>%{label}</b><br>Profit: ₹%{value:,.0f}<br>Share: %{percent}<extra></extra>",
    ))
    fig.add_annotation(
        text="Profit<br>Share",
        x=0.5, y=0.5,
        font=dict(size=11, color=p["muted"]),
        showarrow=False,
    )
    fig.update_layout(title=dict(text="Profit contribution by category", x=0))
    return _themed(fig, dark)


# ── 3. Revenue vs profit bar ──────────────────────────────────────────────────

def revenue_profit_bar(products: pd.DataFrame, dark: bool) -> go.Figure:
    p = palette(dark)
    top = products.head(15).sort_values("gross_revenue", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top["sku"],
        x=top["gross_revenue"],
        name="Gross revenue",
        orientation="h",
        marker=dict(color=p["accent4"], opacity=0.85),
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=top["sku"],
        x=top["return_adjusted_profit"],
        name="Real profit",
        orientation="h",
        marker=dict(
            color=[p["accent6"] if v >= 0 else p["accent3"]
                   for v in top["return_adjusted_profit"]],
            opacity=0.9,
        ),
        hovertemplate="<b>%{y}</b><br>Profit: ₹%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Revenue vs return-adjusted profit – top 15 SKUs", x=0),
        barmode="group",
        xaxis_title="₹",
        yaxis=dict(automargin=True),
    )
    return _themed(fig, dark)


# ── 4. Return reason bar ─────────────────────────────────────────────────────

def return_reason_bar(filtered: pd.DataFrame, dark: bool) -> go.Figure:
    p = palette(dark)
    reason = (
        filtered[filtered["returned"]]
        .groupby("return_reason", as_index=False)
        .agg(refunds=("refund_amount", "sum"), reverse=("return_logistics_cost", "sum"))
    )
    reason["total"] = reason["refunds"] + reason["reverse"]
    reason = reason.sort_values("total", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=reason["return_reason"],
        x=reason["refunds"],
        name="Refunds",
        orientation="h",
        marker=dict(color=p["accent3"], opacity=0.85),
    ))
    fig.add_trace(go.Bar(
        y=reason["return_reason"],
        x=reason["reverse"],
        name="Reverse logistics",
        orientation="h",
        marker=dict(color=p["accent1"], opacity=0.85),
    ))
    fig.update_layout(
        title=dict(text="Return leakage by reason", x=0),
        barmode="stack",
        xaxis_title="₹ leakage",
        yaxis=dict(automargin=True),
    )
    return _themed(fig, dark)


# ── 5. Size heatmap ───────────────────────────────────────────────────────────

def size_heatmap_fig(heatmap: pd.DataFrame, dark: bool) -> go.Figure:
    p = palette(dark)
    pivot = heatmap.pivot_table(index="category", columns="size", values="return_rate", aggfunc="mean")
    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[
            [0.0, p["accent6"] + "80"],
            [0.5, p["accent4"]],
            [1.0, p["accent3"]],
        ],
        hoverongaps=False,
        hovertemplate="Category: %{y}<br>Size: %{x}<br>Return rate: %{z:.1%}<extra></extra>",
        colorbar=dict(
            title=dict(text="Return rate", side="right"),
            tickformat=".0%",
            tickfont=dict(color=p["muted"], size=10),
        ),
    ))
    fig.update_layout(title=dict(text="Return rate by category & size", x=0))
    return _themed(fig, dark)


# ── 6. City tier scatter ──────────────────────────────────────────────────────

def tier_scatter(tiers_df: pd.DataFrame, dark: bool) -> go.Figure:
    p = palette(dark)
    colors = cat_colors(dark)
    fig = go.Figure()
    for i, (_, row) in enumerate(tiers_df.iterrows()):
        fig.add_trace(go.Scatter(
            x=[row["return_rate"]],
            y=[row["return_adjusted_profit"]],
            mode="markers+text",
            name=row["city_tier"],
            marker=dict(
                size=max(12, row.get("orders", 1000) / 500),
                color=colors[i % len(colors)],
                opacity=0.9,
                line=dict(width=1.5, color=p["surface"]),
            ),
            text=[row["city_tier"]],
            textposition="top center",
            textfont=dict(size=11),
            hovertemplate=(
                f"<b>{row['city_tier']}</b><br>"
                "Return rate: %{x:.1%}<br>"
                "Profit: ₹%{y:,.0f}<extra></extra>"
            ),
        ))
    fig.update_layout(
        title=dict(text="City tier – return rate vs profit", x=0),
        xaxis_title="Return rate",
        yaxis_title="Return-adjusted profit (₹)",
        showlegend=False,
    )
    return _themed(fig, dark)


# ── 7. Inventory risk bubble ─────────────────────────────────────────────────

def inventory_risk_fig(inventory: pd.DataFrame, dark: bool) -> go.Figure:
    p = palette(dark)
    top = inventory.head(20)
    fig = go.Figure(go.Scatter(
        x=top["stockout_risk"],
        y=top["markdown_risk"],
        mode="markers",
        marker=dict(
            size=top["risk_score"] * 40 + 8,
            color=top["return_rate"],
            colorscale=[
                [0.0, p["accent6"] + "AA"],
                [0.5, p["accent4"]],
                [1.0, p["accent3"]],
            ],
            opacity=0.85,
            showscale=True,
            colorbar=dict(
                title=dict(text="Return rate", side="right"),
                tickformat=".0%",
                tickfont=dict(color=p["muted"], size=10),
            ),
            line=dict(width=1, color=p["surface"]),
        ),
        text=top["sku"],
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Stockout risk: %{x:.0%}<br>"
            "Markdown risk: %{y:.0%}<br>"
            "<extra></extra>"
        ),
    ))
    fig.update_layout(
        title=dict(text="Inventory risk – stockout vs markdown vs returns", x=0),
        xaxis_title="Stockout risk",
        yaxis_title="Markdown risk",
    )
    return _themed(fig, dark)


# ── 8. Cohort figure ──────────────────────────────────────────────────────────

def cohort_fig(cohorts: pd.DataFrame, dark: bool) -> go.Figure:
    p = palette(dark)
    colors = cat_colors(dark)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=cohorts["cohort_month"].astype(str),
        y=cohorts["avg_profit"],
        name="Avg profit",
        marker=dict(color=colors[0], opacity=0.85),
        hovertemplate="Month: %{x}<br>Avg profit: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=cohorts["cohort_month"].astype(str),
        y=cohorts["repeat_rate"],
        name="Repeat rate",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color=colors[1], width=2.5, dash="dot"),
        marker=dict(size=6, color=colors[1]),
        hovertemplate="Month: %{x}<br>Repeat rate: %{y:.1%}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Customer cohorts – avg profit & repeat rate", x=0),
        xaxis_title="Cohort month",
        yaxis=dict(title="Avg profit (₹)"),
        yaxis2=dict(
            title="Repeat rate",
            overlaying="y",
            side="right",
            tickformat=".0%",
            showgrid=False,
        ),
    )
    return _themed(fig, dark)
