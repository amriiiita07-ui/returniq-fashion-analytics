-- ReturnIQ Fashion Analytics: interview-ready SQL questions
-- The syntax is ANSI-friendly and works with DuckDB, BigQuery, PostgreSQL, or SQLite with small edits.

-- 1. Which bestselling SKUs become loss-makers after returns?
SELECT
    sku,
    product_name,
    category,
    COUNT(*) AS orders,
    SUM(gross_revenue) AS gross_revenue,
    SUM(return_adjusted_profit) AS return_adjusted_profit,
    AVG(CASE WHEN returned THEN 1.0 ELSE 0.0 END) AS return_rate
FROM fashion_orders
GROUP BY sku, product_name, category
HAVING SUM(gross_revenue) > 100000
   AND SUM(return_adjusted_profit) < 0
ORDER BY gross_revenue DESC;

-- 2. Return-adjusted profitability by category and month.
SELECT
    DATE_TRUNC('month', order_date) AS month,
    category,
    SUM(gross_revenue) AS gross_revenue,
    SUM(return_adjusted_profit) AS return_adjusted_profit,
    SUM(return_adjusted_profit) / NULLIF(SUM(gross_revenue), 0) AS return_adjusted_margin
FROM fashion_orders
GROUP BY 1, 2
ORDER BY 1, 2;

-- 3. Size-category return heatmap source table.
SELECT
    category,
    size,
    COUNT(*) AS orders,
    AVG(CASE WHEN returned THEN 1.0 ELSE 0.0 END) AS return_rate,
    SUM(refund_amount + return_logistics_cost) AS return_leakage
FROM fashion_orders
WHERE size <> 'One Size'
GROUP BY category, size
ORDER BY category, size;

-- 4. India city-tier profitability.
SELECT
    city_tier,
    state,
    city,
    COUNT(*) AS orders,
    SUM(gross_revenue) AS gross_revenue,
    SUM(return_adjusted_profit) AS return_adjusted_profit,
    AVG(CASE WHEN returned THEN 1.0 ELSE 0.0 END) AS return_rate
FROM fashion_orders
GROUP BY city_tier, state, city
ORDER BY return_adjusted_profit DESC;

-- 5. Return reasons by refund leakage.
SELECT
    return_reason,
    COUNT(*) AS returned_orders,
    SUM(refund_amount) AS refunds,
    SUM(return_logistics_cost) AS reverse_logistics_cost,
    SUM(refund_amount + return_logistics_cost) AS total_leakage
FROM fashion_orders
WHERE returned = TRUE
GROUP BY return_reason
ORDER BY total_leakage DESC;

-- 6. Channel quality after returns.
SELECT
    channel,
    COUNT(*) AS orders,
    SUM(gross_revenue) AS gross_revenue,
    AVG(CASE WHEN returned THEN 1.0 ELSE 0.0 END) AS return_rate,
    SUM(return_adjusted_profit) / NULLIF(COUNT(*), 0) AS profit_per_order
FROM fashion_orders
GROUP BY channel
ORDER BY profit_per_order DESC;

-- 7. Inventory risk shortlist.
SELECT
    sku,
    product_name,
    category,
    SUM(units) AS units_sold,
    AVG(inventory_on_hand) AS avg_inventory,
    AVG(stockout_risk) AS stockout_risk,
    AVG(markdown_risk) AS markdown_risk,
    AVG(CASE WHEN returned THEN 1.0 ELSE 0.0 END) AS return_rate,
    SUM(return_adjusted_profit) AS return_adjusted_profit
FROM fashion_orders
GROUP BY sku, product_name, category
ORDER BY (AVG(stockout_risk) * 0.32 + AVG(markdown_risk) * 0.32 + AVG(CASE WHEN returned THEN 1.0 ELSE 0.0 END) * 0.36) DESC;

