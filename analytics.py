from __future__ import annotations

import pandas as pd


MONEY_COLUMNS = [
    "gross_revenue",
    "discount",
    "net_sales",
    "product_cost",
    "shipping_cost",
    "payment_fee",
    "return_logistics_cost",
    "refund_amount",
    "return_adjusted_profit",
]


def prepare_orders(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["order_date"] = pd.to_datetime(data["order_date"])
    data["month"] = data["order_date"].dt.to_period("M").astype(str)
    data["returned"] = data["returned"].astype(bool)
    for column in MONEY_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce").fillna(0)
    data["return_adjusted_margin"] = data["return_adjusted_profit"] / data["gross_revenue"].replace(0, pd.NA)
    data["return_adjusted_margin"] = data["return_adjusted_margin"].fillna(0)
    data["profit_status"] = data["return_adjusted_profit"].map(lambda value: "Profitable" if value >= 0 else "Loss-maker")
    return data


def filter_orders(
    df: pd.DataFrame,
    categories: list[str],
    tiers: list[str],
    channels: list[str],
    date_range: tuple[pd.Timestamp, pd.Timestamp],
) -> pd.DataFrame:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    mask = (
        df["category"].isin(categories)
        & df["city_tier"].isin(tiers)
        & df["channel"].isin(channels)
        & df["order_date"].between(start, end)
    )
    return df.loc[mask].copy()


def kpis(df: pd.DataFrame) -> dict[str, float]:
    orders = len(df)
    gross = float(df["gross_revenue"].sum())
    profit = float(df["return_adjusted_profit"].sum())
    returns = float(df["returned"].mean()) if orders else 0.0
    margin = profit / gross if gross else 0.0
    refund_leakage = float((df["refund_amount"] + df["return_logistics_cost"]).sum())
    aov = float(df["gross_revenue"].sum() / orders) if orders else 0.0
    return {
        "orders": orders,
        "gross_revenue": gross,
        "return_adjusted_profit": profit,
        "return_rate": returns,
        "return_adjusted_margin": margin,
        "refund_leakage": refund_leakage,
        "aov": aov,
    }


def product_profitability(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(["sku", "product_name", "category", "size"], as_index=False)
        .agg(
            orders=("order_id", "count"),
            units=("units", "sum"),
            gross_revenue=("gross_revenue", "sum"),
            returned_units=("returned", "sum"),
            refund_amount=("refund_amount", "sum"),
            return_logistics_cost=("return_logistics_cost", "sum"),
            return_adjusted_profit=("return_adjusted_profit", "sum"),
        )
    )
    grouped["return_rate"] = grouped["returned_units"] / grouped["orders"].replace(0, pd.NA)
    grouped["profit_rate"] = grouped["return_adjusted_profit"] / grouped["gross_revenue"].replace(0, pd.NA)
    grouped["revenue_rank"] = grouped["gross_revenue"].rank(ascending=False, method="dense").astype(int)
    grouped["profit_rank"] = grouped["return_adjusted_profit"].rank(ascending=False, method="dense").astype(int)
    grouped["rank_flip"] = grouped["profit_rank"] - grouped["revenue_rank"]
    return grouped.sort_values("gross_revenue", ascending=False)


def category_monthly(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["month", "category"], as_index=False)
        .agg(
            gross_revenue=("gross_revenue", "sum"),
            return_adjusted_profit=("return_adjusted_profit", "sum"),
            return_rate=("returned", "mean"),
            orders=("order_id", "count"),
        )
        .sort_values(["month", "category"])
    )


def size_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    pivot = pd.pivot_table(
        df[df["size"] != "One Size"],
        values="returned",
        index="category",
        columns="size",
        aggfunc="mean",
        fill_value=0,
    )
    preferred = ["XS", "S", "M", "L", "XL", "XXL"]
    return pivot.reindex(columns=[size for size in preferred if size in pivot.columns])


def city_tier_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby(["city_tier", "state"], as_index=False)
        .agg(
            orders=("order_id", "count"),
            gross_revenue=("gross_revenue", "sum"),
            return_rate=("returned", "mean"),
            return_adjusted_profit=("return_adjusted_profit", "sum"),
        )
    )
    summary["profit_per_order"] = summary["return_adjusted_profit"] / summary["orders"].replace(0, pd.NA)
    return summary.sort_values("return_adjusted_profit", ascending=False)


def cohort_summary(df: pd.DataFrame) -> pd.DataFrame:
    customer_orders = df.sort_values("order_date").groupby("customer_id").agg(
        first_month=("cohort_month", "first"),
        orders=("order_id", "count"),
        gross_revenue=("gross_revenue", "sum"),
        profit=("return_adjusted_profit", "sum"),
        returned_any=("returned", "max"),
    )
    return (
        customer_orders.groupby("first_month", as_index=False)
        .agg(
            customers=("orders", "count"),
            repeat_rate=("orders", lambda values: (values > 1).mean()),
            avg_revenue=("gross_revenue", "mean"),
            avg_profit=("profit", "mean"),
            returner_rate=("returned_any", "mean"),
        )
        .sort_values("first_month")
    )


def inventory_risk(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(["sku", "product_name", "category"], as_index=False)
        .agg(
            units_sold=("units", "sum"),
            gross_revenue=("gross_revenue", "sum"),
            return_adjusted_profit=("return_adjusted_profit", "sum"),
            avg_inventory=("inventory_on_hand", "mean"),
            stockout_risk=("stockout_risk", "mean"),
            markdown_risk=("markdown_risk", "mean"),
            return_rate=("returned", "mean"),
        )
    )
    grouped["risk_score"] = (
        grouped["stockout_risk"] * 0.32
        + grouped["markdown_risk"] * 0.32
        + grouped["return_rate"] * 0.36
    )
    return grouped.sort_values("risk_score", ascending=False)

