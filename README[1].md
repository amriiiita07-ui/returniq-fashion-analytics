# ReturnIQ Fashion Analytics

ReturnIQ is an industry-style fashion e-commerce analytics project focused on the question most sales dashboards avoid:

> Which products are still profitable after returns, discounts, logistics, and category-specific costs?

The app is built with Streamlit, Pandas, Plotly, and SQL-ready datasets. It includes a synthetic Indian fashion marketplace dataset with product, size, city-tier, channel, customer, margin, and return behavior.

## What Makes This Portfolio Project Different

- Return-adjusted profitability score for every SKU and category.
- Bestseller flip analysis that compares gross revenue winners against net-profit winners.
- Size and fit return heatmaps for apparel categories.
- Tier 1, Tier 2, and Tier 3 Indian city analysis.
- Customer cohorts, repeat behavior, refund leakage, and return risk.
- Inventory risk and demand forecast views.
- SQL analysis file for interview-ready business questions.
- Polished light/dark dashboard UI with multiple tabs, KPI cards, rich charts, and tables.

## Project Structure

```text
returniq-fashion-analytics/
  app.py
  requirements.txt
  README.md
  .streamlit/
    config.toml
  data/
    fashion_orders_sample.csv
  sql/
    analysis_queries.sql
  src/
    analytics.py
    charts.py
    data_generator.py
    styles.py
  tests/
    test_analytics.py
```

## Run Locally

1. Create a virtual environment.

```bash
python -m venv .venv
```

2. Activate it.

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Start the dashboard.

```bash
streamlit run app.py
```

5. Open the local URL Streamlit prints in your terminal, usually:

```text
http://localhost:8501
```

## Main Dashboard Tabs

- Command Center: leadership KPIs, return-adjusted profit trend, category split.
- Profitability Flip: shows how top sellers can become loss-makers after returns.
- Returns Lab: return reasons, refund leakage, high-risk categories.
- Size Intelligence: size-category return heatmaps and fit-risk insights.
- India City Tiers: Tier 1/2/3 market behavior and state-level performance.
- Inventory Risk: markdown exposure, stockout risk, dead-stock flags.
- Customer Cohorts: acquisition cohorts, repeat rate, customer lifetime signals.
- Data Lab: downloadable data, schema notes, and SQL interview questions.

## Key Metric

```text
Return Adjusted Profit =
Gross Revenue
- Discounts
- Product Cost
- Shipping Cost
- Payment Fees
- Return Logistics Cost
- Refund Amount
```

```text
Return Adjusted Profitability Rate =
Return Adjusted Profit / Gross Revenue
```

## GitHub Upload Guide

1. Create a new GitHub repository.
2. Extract the zip file if you received this project as an archive.
3. Open a terminal inside the project folder.
4. Run:

```bash
git init
git add .
git commit -m "Initial ReturnIQ fashion analytics project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

5. Add screenshots and a short demo GIF to your README after you run the app.

## Suggested Portfolio Story

Use this project as a case study:

1. Start with the business problem: revenue hides return losses.
2. Show the bestseller flip: top revenue SKUs are not always top profit SKUs.
3. Prove the source of leakage: size/category return heatmaps.
4. Localize the insight: city-tier differences in Indian fashion shopping behavior.
5. End with actions: fit guidance, stock reallocation, category margin repair, and returns policy changes.

