from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def palette(dark_mode: bool) -> dict[str, object]:
    return {
        "template": "plotly_dark" if dark_mode else "plotly_white",
        "colors": ["#f97316", "#22c55e", "#0ea5e9", "#e11d48", "#a855f7", "#facc15", "#14b8a6"],
        "paper": "rgba(0,0,0,0)",
        "plot": "rgba(0,0,0,0)",
        "font": "#f8fafc" if dark_mode else "#0f172a",
        "grid": "rgba(148,163,184,0.16)" if dark_mode else "rgba(100,116,139,0.16)",
    }


def polish(fig: go.Figure, dark_mode: bool, height: int = 380) -> go.Figure:
    p = palette(dark_mode)
    fig.update_layout(
        template=p["template"],
        height=height,
        paper_bgcolor=p["paper"],
        plot_bgcolor=p["plot"],
        font_color=p["font"],
        margin=dict(l=14, r=14, t=48, b=16),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(gridcolor=p["grid"], zerolinecolor=p["grid"])
    fig.update_yaxes(gridcolor=p["grid"], zerolinecolor=p["grid"])
    return fig


def monthly_profit_line(df: pd.DataFrame, dark_mode: bool) -> go.Figure:
    p = palette(dark_mode)
    fig = px.line(
        df,
        x="month",
        y="return_adjusted_profit",
        color="category",
        markers=True,
        color_discrete_sequence=p["colors"],
        title="Return-adjusted profit by month",
    )
    return polish(fig, dark_mode, 410)


def revenue_profit_bar(df: pd.DataFrame, dark_mode: bool) -> go.Figure:
    top = df.head(12).sort_values("gross_revenue")
    fig = go.Figure()
    fig.add_bar(y=top["sku"], x=top["gross_revenue"], orientation="h", name="Gross revenue", marker_color="#0ea5e9")
    fig.add_bar(y=top["sku"], x=top["return_adjusted_profit"], orientation="h", name="Return-adjusted profit", marker_color="#f97316")
    fig.update_layout(title="Bestseller flip: revenue vs real profit", barmode="group")
    return polish(fig, dark_mode, 470)


def return_reason_bar(df: pd.DataFrame, dark_mode: bool) -> go.Figure:
    reasons = (
        df[df["returned"]]
        .groupby("return_reason", as_index=False)
        .agg(orders=("order_id", "count"), leakage=("refund_amount", "sum"))
        .sort_values("orders", ascending=True)
    )
    fig = px.bar(
        reasons,
        y="return_reason",
        x="orders",
        color="leakage",
        orientation="h",
        color_continuous_scale=["#22c55e", "#f97316", "#e11d48"],
        title="Why customers return fashion orders",
    )
    return polish(fig, dark_mode, 390)


def size_heatmap_fig(heatmap: pd.DataFrame, dark_mode: bool) -> go.Figure:
    # Reset named index/columns from pivot_table — px.imshow renders blank otherwise
    clean = heatmap.copy()
    clean.index.name = None
    clean.columns.name = None
    fig = px.imshow(
        clean,
        text_auto=".0%",
        aspect="auto",
        color_continuous_scale=["#0f766e", "#facc15", "#e11d48"],
        title="Size-category return rate heatmap",
        labels=dict(x="Size", y="Category", color="Return rate"),
    )
    fig.update_traces(textfont_size=13)
    return polish(fig, dark_mode, 390)


def tier_scatter(df: pd.DataFrame, dark_mode: bool) -> go.Figure:
    fig = px.scatter(
        df,
        x="return_rate",
        y="profit_per_order",
        size="gross_revenue",
        color="city_tier",
        hover_name="state",
        color_discrete_sequence=palette(dark_mode)["colors"],
        title="City-tier return risk vs profit per order",
    )
    fig.update_xaxes(tickformat=".0%")
    return polish(fig, dark_mode, 410)


def cohort_fig(df: pd.DataFrame, dark_mode: bool) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["first_month"], y=df["customers"], name="Customers", marker_color="#0ea5e9"))
    fig.add_trace(go.Scatter(x=df["first_month"], y=df["repeat_rate"], name="Repeat rate", yaxis="y2", mode="lines+markers", marker_color="#f97316"))
    fig.update_layout(
        title="Customer cohorts: acquisition volume and repeat behavior",
        yaxis=dict(title="Customers"),
        yaxis2=dict(title="Repeat rate", overlaying="y", side="right", tickformat=".0%"),
    )
    return polish(fig, dark_mode, 410)


def inventory_risk_fig(df: pd.DataFrame, dark_mode: bool) -> go.Figure:
    top = df.head(18)
    fig = px.scatter(
        top,
        x="stockout_risk",
        y="markdown_risk",
        size="gross_revenue",
        color="return_rate",
        hover_name="sku",
        color_continuous_scale=["#22c55e", "#f97316", "#e11d48"],
        title="Inventory risk map: stockout pressure vs markdown exposure",
    )
    fig.update_xaxes(tickformat=".0%")
    fig.update_yaxes(tickformat=".0%")
    return polish(fig, dark_mode, 410)


def category_donut(df: pd.DataFrame, dark_mode: bool) -> go.Figure:
    grouped = df.groupby("category", as_index=False)["return_adjusted_profit"].sum()
    grouped["display_profit"] = grouped["return_adjusted_profit"].clip(lower=0)
    if grouped["display_profit"].sum() == 0:
        grouped["display_profit"] = grouped["return_adjusted_profit"].abs()
    fig = px.pie(
        grouped,
        names="category",
        values="display_profit",
        hole=0.58,
        color_discrete_sequence=palette(dark_mode)["colors"],
        title="Profit contribution by category",
    )
    return polish(fig, dark_mode, 370)
