from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.analytics import (
    category_monthly,
    city_tier_summary,
    cohort_summary,
    filter_orders,
    inventory_risk,
    kpis,
    prepare_orders,
    product_profitability,
    size_heatmap,
)
from src.charts import (
    category_donut,
    cohort_fig,
    inventory_risk_fig,
    monthly_profit_line,
    return_reason_bar,
    revenue_profit_bar,
    size_heatmap_fig,
    tier_scatter,
)
from src.data_generator import ensure_sample_data
from src.styles import app_css, metric_card


APP_ROOT = Path(__file__).parent
DATA_PATH = APP_ROOT / "data" / "fashion_orders_sample.csv"


st.set_page_config(
    page_title="ReturnIQ Fashion Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    ensure_sample_data(DATA_PATH)
    return prepare_orders(pd.read_csv(DATA_PATH))


def money(value: float) -> str:
    abs_value = abs(value)
    sign = "-" if value < 0 else ""
    if abs_value >= 10_000_000:
        return f"{sign}₹{abs_value / 10_000_000:.2f}Cr"
    if abs_value >= 100_000:
        return f"{sign}₹{abs_value / 100_000:.2f}L"
    return f"{sign}₹{abs_value:,.0f}"


def pct(value: float) -> str:
    return f"{value:.1%}"


def render_topbar(dark_mode: bool) -> None:
    st.markdown(
        """
        <div class="topbar">
          <div class="brand-lockup">
            <div class="logo-mark">RIQ</div>
            <div>
              <p class="eyebrow">Fashion e-commerce analytics suite</p>
              <h1 class="app-title">ReturnIQ Profitability Command Center</h1>
            </div>
          </div>
          <div class="eyebrow">Built for return-aware merchandising decisions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_grid(metrics: dict[str, float]) -> None:
    columns = st.columns(6)
    values = [
        ("Orders", f"{metrics['orders']:,}", "Filtered transactions"),
        ("Gross Revenue", money(metrics["gross_revenue"]), "Before returns"),
        ("Real Profit", money(metrics["return_adjusted_profit"]), "After refunds and reverse logistics"),
        ("Return Rate", pct(metrics["return_rate"]), "Customer return behavior"),
        ("RA Margin", pct(metrics["return_adjusted_margin"]), "Profit / gross revenue"),
        ("AOV", money(metrics["aov"]), "Average order value"),
    ]
    for column, (label, value, delta) in zip(columns, values):
        column.markdown(metric_card(label, value, delta), unsafe_allow_html=True)


orders = load_data()

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

top_left, top_right = st.columns([0.82, 0.18])
with top_right:
    dark_mode = st.toggle("◐ Theme", value=st.session_state.dark_mode, help="Switch light and dark mode.")
    st.session_state.dark_mode = dark_mode

with st.sidebar:
    st.caption("ReturnIQ controls")
    st.divider()
    categories = st.multiselect("Categories", sorted(orders["category"].unique()), default=sorted(orders["category"].unique()))
    tiers = st.multiselect("City tiers", sorted(orders["city_tier"].unique()), default=sorted(orders["city_tier"].unique()))
    channels = st.multiselect("Channels", sorted(orders["channel"].unique()), default=sorted(orders["channel"].unique()))
    min_date = orders["order_date"].min().date()
    max_date = orders["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if len(date_range) != 2:
        date_range = (min_date, max_date)
    st.divider()
    st.download_button(
        "Download filtered CSV",
        data=orders.to_csv(index=False),
        file_name="returniq_fashion_orders.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.markdown(app_css(dark_mode), unsafe_allow_html=True)
render_topbar(dark_mode)

filtered = filter_orders(orders, categories, tiers, channels, date_range)
metrics = kpis(filtered)
products = product_profitability(filtered)
monthly = category_monthly(filtered)
heatmap = size_heatmap(filtered)
tiers_df = city_tier_summary(filtered)
cohorts = cohort_summary(filtered)
inventory = inventory_risk(filtered)

loss_makers = int((products.head(10)["return_adjusted_profit"] < 0).sum())
return_leakage = metrics["refund_leakage"]

st.markdown(
    f"""
    <div class="hero-grid">
      <div class="hero-panel">
        <p class="eyebrow">Core portfolio thesis</p>
        <h2 class="app-title">Revenue is vanity. Return-adjusted profit is the truth.</h2>
        <p class="hero-copy">
          This dashboard models a fashion marketplace where discounts, refunds, payment fees,
          product cost, forward shipping, and reverse logistics are all included. The result is
          a recruiter-friendly analytics story: the products that look like winners can quietly
          destroy profit after returns.
        </p>
      </div>
      <div class="insight-panel">
        <div class="insight-label">Bestseller flip signal</div>
        <div class="insight-number">{loss_makers}/10</div>
        <div class="insight-text">
          top revenue SKUs are net loss-makers in the current filter. Total refund and return
          logistics leakage is <strong>{money(return_leakage)}</strong>.
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

render_metric_grid(metrics)

tabs = st.tabs(
    [
        "Command Center",
        "Profitability Flip",
        "Returns Lab",
        "Size Intelligence",
        "India City Tiers",
        "Inventory Risk",
        "Customer Cohorts",
        "Channel Mix",
        "Data Lab",
    ]
)

with tabs[0]:
    st.markdown('<div class="section-title">Executive view</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">High-level performance after accounting for return economics.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.55, 1])
    with col1:
        fig = monthly_profit_line(monthly, dark_mode)
fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=80)
)
st.plotly_chart(fig, use_container_width=True)
       
    with col2:
        fig2 = category_donut(filtered, dark_mode)
fig2.update_layout(
    margin=dict(t=80)
)
st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(
        monthly.sort_values("return_adjusted_profit", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "gross_revenue": st.column_config.NumberColumn("Gross revenue", format="₹%.0f"),
            "return_adjusted_profit": st.column_config.NumberColumn("Return-adjusted profit", format="₹%.0f"),
            "return_rate": st.column_config.ProgressColumn("Return rate", min_value=0, max_value=1, format="%.1f"),
        },
    )

with tabs[1]:
    st.markdown('<div class="section-title">The bestseller flip</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">A SKU can rank high in revenue and still lose money after return costs.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.plotly_chart(revenue_profit_bar(products, dark_mode), use_container_width=True)
    with col2:
        flip_table = products.sort_values("rank_flip", ascending=False).head(12)
        st.dataframe(
            flip_table[
                [
                    "sku",
                    "category",
                    "gross_revenue",
                    "return_adjusted_profit",
                    "return_rate",
                    "revenue_rank",
                    "profit_rank",
                    "rank_flip",
                ]
            ],
            use_container_width=True,
            hide_index=True,
            column_config={
                "gross_revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f"),
                "return_adjusted_profit": st.column_config.NumberColumn("Real profit", format="₹%.0f"),
                "return_rate": st.column_config.ProgressColumn("Return rate", min_value=0, max_value=1, format="%.1f"),
            },
        )
    st.download_button(
        "Download SKU profitability table",
        products.to_csv(index=False),
        file_name="sku_return_adjusted_profitability.csv",
        mime="text/csv",
    )

with tabs[2]:
    st.markdown('<div class="section-title">Returns lab</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">Pinpoint the operational reasons behind leakage and refund drag.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.15, 1])
    with col1:
        st.plotly_chart(return_reason_bar(filtered, dark_mode), use_container_width=True)
    with col2:
        reason_table = (
            filtered[filtered["returned"]]
            .groupby("return_reason", as_index=False)
            .agg(orders=("order_id", "count"), refunds=("refund_amount", "sum"), reverse_logistics=("return_logistics_cost", "sum"))
        )
        reason_table["total_leakage"] = reason_table["refunds"] + reason_table["reverse_logistics"]
        reason_table = reason_table.sort_values("total_leakage", ascending=False)
        st.dataframe(
            reason_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "refunds": st.column_config.NumberColumn("Refunds", format="₹%.0f"),
                "reverse_logistics": st.column_config.NumberColumn("Reverse logistics", format="₹%.0f"),
                "total_leakage": st.column_config.NumberColumn("Total leakage", format="₹%.0f"),
            },
        )

with tabs[3]:
    st.markdown('<div class="section-title">Size intelligence</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">Sizing is treated as a measurable product-data problem.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.25, 1])
    with col1:
        st.plotly_chart(size_heatmap_fig(heatmap, dark_mode), use_container_width=True)
    with col2:
        size_table = (
            filtered[filtered["size"] != "One Size"]
            .groupby(["category", "size"], as_index=False)
            .agg(orders=("order_id", "count"), return_rate=("returned", "mean"), profit=("return_adjusted_profit", "sum"))
            .sort_values("return_rate", ascending=False)
            .head(15)
        )
        st.dataframe(
            size_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "return_rate": st.column_config.ProgressColumn("Return rate", min_value=0, max_value=1, format="%.1f"),
                "profit": st.column_config.NumberColumn("Profit", format="₹%.0f"),
            },
        )

with tabs[4]:
    st.markdown('<div class="section-title">India city-tier lens</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">Compare profitability across Tier 1, Tier 2, and Tier 3 demand pockets.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.plotly_chart(tier_scatter(tiers_df, dark_mode), use_container_width=True)
    with col2:
        tier_cards = filtered.groupby("city_tier", as_index=False).agg(
            orders=("order_id", "count"),
            profit=("return_adjusted_profit", "sum"),
            return_rate=("returned", "mean"),
        )
        for _, row in tier_cards.iterrows():
            st.markdown(metric_card(row["city_tier"], money(row["profit"]), f"{int(row['orders']):,} orders · {pct(row['return_rate'])} returns"), unsafe_allow_html=True)
    st.dataframe(
        tiers_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "gross_revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f"),
            "return_adjusted_profit": st.column_config.NumberColumn("Real profit", format="₹%.0f"),
            "return_rate": st.column_config.ProgressColumn("Return rate", min_value=0, max_value=1, format="%.1f"),
            "profit_per_order": st.column_config.NumberColumn("Profit/order", format="₹%.0f"),
        },
    )

with tabs[5]:
    st.markdown('<div class="section-title">Inventory risk</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">Find SKUs where stock pressure, markdown risk, and return rate collide.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.25, 1])
    with col1:
        st.plotly_chart(inventory_risk_fig(inventory, dark_mode), use_container_width=True)
    with col2:
        st.dataframe(
            inventory.head(18),
            use_container_width=True,
            hide_index=True,
            column_config={
                "gross_revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f"),
                "return_adjusted_profit": st.column_config.NumberColumn("Profit", format="₹%.0f"),
                "stockout_risk": st.column_config.ProgressColumn("Stockout", min_value=0, max_value=1, format="%.1f"),
                "markdown_risk": st.column_config.ProgressColumn("Markdown", min_value=0, max_value=1, format="%.1f"),
                "return_rate": st.column_config.ProgressColumn("Returns", min_value=0, max_value=1, format="%.1f"),
                "risk_score": st.column_config.ProgressColumn("Risk score", min_value=0, max_value=1, format="%.1f"),
            },
        )

with tabs[6]:
    st.markdown('<div class="section-title">Customer cohorts</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">Track acquisition quality, repeat rate, and returner behavior by first purchase month.</p>', unsafe_allow_html=True)
    st.plotly_chart(cohort_fig(cohorts, dark_mode), use_container_width=True)
    st.dataframe(
        cohorts,
        use_container_width=True,
        hide_index=True,
        column_config={
            "repeat_rate": st.column_config.ProgressColumn("Repeat rate", min_value=0, max_value=1, format="%.1f"),
            "avg_revenue": st.column_config.NumberColumn("Avg revenue", format="₹%.0f"),
            "avg_profit": st.column_config.NumberColumn("Avg profit", format="₹%.0f"),
            "returner_rate": st.column_config.ProgressColumn("Returner rate", min_value=0, max_value=1, format="%.1f"),
        },
    )

with tabs[7]:
    st.markdown('<div class="section-title">Channel mix</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">Separate high-volume channels from channels that produce durable profit.</p>', unsafe_allow_html=True)
    channel_table = (
        filtered.groupby("channel", as_index=False)
        .agg(
            orders=("order_id", "count"),
            gross_revenue=("gross_revenue", "sum"),
            return_rate=("returned", "mean"),
            profit=("return_adjusted_profit", "sum"),
        )
        .sort_values("profit", ascending=False)
    )
    channel_table["profit_per_order"] = channel_table["profit"] / channel_table["orders"]
    col1, col2 = st.columns([1.1, 1])
    with col1:
        st.bar_chart(channel_table.set_index("channel")[["gross_revenue", "profit"]], use_container_width=True)
    with col2:
        st.dataframe(
            channel_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "gross_revenue": st.column_config.NumberColumn("Revenue", format="₹%.0f"),
                "return_rate": st.column_config.ProgressColumn("Return rate", min_value=0, max_value=1, format="%.1f"),
                "profit": st.column_config.NumberColumn("Profit", format="₹%.0f"),
                "profit_per_order": st.column_config.NumberColumn("Profit/order", format="₹%.0f"),
            },
        )

with tabs[8]:
    st.markdown('<div class="section-title">Data lab</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-note">Use this tab to explain the dataset, export files, and discuss SQL during interviews.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Dataset schema")
        st.dataframe(
            pd.DataFrame(
                {
                    "column": filtered.columns,
                    "dtype": [str(dtype) for dtype in filtered.dtypes],
                    "example": [str(filtered[column].iloc[0]) if len(filtered) else "" for column in filtered.columns],
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
    with col2:
        st.subheader("Interview SQL prompts")
        st.markdown(
            """
            - Which top revenue SKUs are net loss-makers?
            - Which size-category combinations drive the most leakage?
            - How does Tier 2 profitability compare with Tier 1?
            - Which channel has the best profit per order after returns?
            - Which SKUs should merchandising fix before adding inventory?
            """
        )
        st.download_button(
            "Download SQL query pack",
            data=(APP_ROOT / "sql" / "analysis_queries.sql").read_text(encoding="utf-8"),
            file_name="returniq_analysis_queries.sql",
            mime="text/sql",
            use_container_width=True,
        )
        st.download_button(
            "Download filtered dataset",
            data=filtered.to_csv(index=False),
            file_name="returniq_filtered_orders.csv",
            mime="text/csv",
            use_container_width=True,
        )
