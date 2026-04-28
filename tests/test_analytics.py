from src.analytics import kpis, prepare_orders, product_profitability
from src.data_generator import generate_orders


def test_generated_data_has_return_profit_columns():
    df = prepare_orders(generate_orders(rows=250, seed=7))
    assert "return_adjusted_profit" in df.columns
    assert "return_adjusted_margin" in df.columns
    assert len(df) == 250


def test_kpis_are_consistent():
    df = prepare_orders(generate_orders(rows=100, seed=11))
    result = kpis(df)
    assert result["orders"] == 100
    assert result["gross_revenue"] > 0
    assert 0 <= result["return_rate"] <= 1


def test_product_profitability_ranks_products():
    df = prepare_orders(generate_orders(rows=500, seed=21))
    products = product_profitability(df)
    assert {"revenue_rank", "profit_rank", "rank_flip"}.issubset(products.columns)
    assert products["orders"].sum() == 500

