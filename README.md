# 🛍️ ReturnIQ — Fashion E-Commerce Profitability Command Center

> **Revenue is vanity. Return-adjusted profit is the truth.**

A full-stack, production-grade analytics dashboard built for Indian fashion e-commerce — where high return rates silently destroy margins. ReturnIQ models every cost layer (discounts, refunds, payment fees, forward & reverse logistics) to surface the *real* profitability story behind every SKU, channel, and city tier.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://returniq-fashion-analytics.streamlit.app)
&nbsp;
![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-lightblue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?logo=plotly)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit)

---

## 📸 Dashboard Preview

| Command Center | Profitability Flip | Inventory Risk |
|---|---|---|
| Monthly profit trends & category donut | Revenue-vs-profit bestseller flip | Stockout × Markdown × Return rate bubble |

---

## 🎯 Why This Project Exists

India's fashion e-commerce sector has **return rates of 25–40%**, often higher than any other category. Most analytics tools stop at gross revenue — a number that is completely misleading when a third of orders come back. This project answers a deceptively simple question:

> **Which products are actually making money after you account for returns?**

ReturnIQ builds a full economic model per order:

```
Real Profit = Selling Price
            − Product Cost
            − Discount
            − Payment Gateway Fee
            − Forward Shipping Cost
            − [If returned] Refund Amount
            − [If returned] Reverse Logistics Cost
```

The result: a dashboard that flips the traditional analytics story on its head — **bestsellers become loss-makers, Tier 2 cities outperform Tier 1, and sizing issues show up as financial risk, not just operational noise.**

---

## 🏗️ Architecture & Project Structure

```
returniq-fashion-analytics/
│
├── app.py                        # Main Streamlit app — layout, tabs, filters
│
├── src/
│   ├── analytics.py              # All business logic & KPI computation
│   ├── charts.py                 # Plotly figure builders (fully themed)
│   ├── styles.py                 # CSS, palette, dark/light theme system
│   └── data_generator.py        # Synthetic data generator (reproducible)
│
├── data/
│   └── fashion_orders_sample.csv # Auto-generated on first run
│
├── sql/
│   └── analysis_queries.sql      # Analyst-ready SQL query pack
│
└── requirements.txt
```

### Design Decisions

| Decision | Reason |
|---|---|
| `@st.cache_data` on data load | Prevents re-processing on every UI interaction |
| Modular `src/` layout | Separation of concerns — analytics logic never touches UI code |
| Synthetic data generator | Zero data privacy risk; fully reproducible; works offline |
| Plotly over `st.bar_chart` | Full theme control, no layout bleeding between columns |
| Dark/light toggle via CSS injection | Single `app_css()` call controls entire visual system |

---

## 📊 Dashboard Tabs — Full Feature Breakdown

### 1. 🖥️ Command Center
**The executive summary.** Monthly return-adjusted profit trend lines broken by category, alongside a profit-share donut. Answers: *Is the business improving month-over-month in real terms?*

- Spline smoothed multi-series line chart
- Donut with 62% hole and annotation
- Sortable summary dataframe

---

### 2. 🔄 Profitability Flip
**The signature insight of this dashboard.** Shows the top 15 SKUs ranked by gross revenue — then overlays their return-adjusted profit. SKUs that rank #1 in revenue but #12 in profit are the "bestseller flip" signal.

- Horizontal grouped bar chart (revenue vs real profit)
- Negative profit bars rendered in red automatically
- `rank_flip` metric = `revenue_rank − profit_rank` (custom engineered feature)
- Full sortable table with download button

---

### 3. 🔬 Returns Lab
**Operational root cause analysis.** Breaks down return leakage by return reason (size issue, quality complaint, wrong item, changed mind, etc.) into refund cost and reverse logistics cost.

- Stacked horizontal bar chart
- Leakage table: refunds + reverse logistics = total drain per reason
- Directly actionable for operations and merchandising teams

---

### 4. 📐 Size Intelligence
**Sizing as a data problem.** In fashion, sizing is the #1 return driver. This tab turns size data into a heatmap — return rate by category × size combination.

- Heatmap with diverging color scale (green → amber → red)
- Pivot table: category × size → mean return rate
- Top 15 highest-return size-category combos in table view
- Graceful fallback if size data is missing for a filter

---

### 5. 🇮🇳 India City Tiers
**India-specific market intelligence.** The Indian e-commerce market segments into Tier 1 (metros), Tier 2 (mid-cities), and Tier 3 (smaller towns) — each with different customer behavior, logistics costs, and return patterns.

- Bubble scatter: return rate vs profit per tier
- Metric cards per tier: profit, order count, return rate
- Full summary dataframe below

---

### 6. 📦 Inventory Risk
**Where stock pressure meets return risk.** Surfaces SKUs that simultaneously face stockout risk (selling fast) AND markdown risk (not selling fast enough) AND high return rates — the triple-threat inventory problem.

- Bubble chart: stockout risk (x) × markdown risk (y) × return rate (color) × risk score (size)
- Composite `risk_score` engineered from three signals
- Full SKU table spanning entire width

---

### 7. 👥 Customer Cohorts
**Acquisition quality over time.** Groups customers by their first purchase month and tracks repeat rate, average profit, and returner rate — answering: *Are we acquiring better or worse customers over time?*

- Dual-axis chart: bar (avg profit) + dotted line (repeat rate)
- Detects cohort month column name automatically (robust to schema changes)
- Full cohort table below

---

### 8. 📡 Channel Mix
**Which channel actually makes money?** Compares gross revenue vs return-adjusted profit across sales channels (app, website, marketplace, social commerce). High-volume channels often have the worst profit-per-order.

- Grouped bar chart with ₹ labels
- `profit_per_order` engineered column
- Full channel table alongside

---

### 9. 🧪 Data Lab
**Interview-ready.** Exposes the full dataset schema with dtypes and example values. Ships with a SQL query pack covering the core analytical questions this dashboard answers.

- Live schema explorer
- SQL prompt pack (downloadable)
- Filtered dataset export

---

## ⚙️ KPIs Computed

| Metric | Formula |
|---|---|
| **Gross Revenue** | `sum(selling_price)` |
| **Return-Adjusted Profit** | `sum(real_profit)` after all cost deductions |
| **Return Rate** | `returned_orders / total_orders` |
| **RA Margin** | `return_adjusted_profit / gross_revenue` |
| **AOV** | `gross_revenue / total_orders` |
| **Refund Leakage** | `sum(refund_amount) + sum(return_logistics_cost)` |
| **Rank Flip** | `revenue_rank − profit_rank` per SKU |
| **Risk Score** | Composite of stockout, markdown, and return risk |

---

## 🎨 Design System

ReturnIQ ships with a full dual-theme design system:

```python
# Dark palette (default)
bg       = "#0D0E12"
surface  = "#14161E"
accent1  = "#FF6B35"   # Orange — primary highlight
accent2  = "#00D4B1"   # Teal — secondary
accent3  = "#E05520"   # Red — loss / risk
accent6  = "#00D4B1"   # Green — profit / safe

# Light palette — full mirror set
```

- All Plotly charts consume `palette(dark)` — one toggle switches every chart
- CSS injected via `app_css(dark_mode)` — controls cards, topbar, hero panel
- `metric_card()` renders HTML cards with consistent typography
- `apply_theme()` in `styles.py` handles legend placement, margins, font globally

---

## 🧠 Key Engineering Decisions

### Synthetic Data Generator
The data generator (`src/data_generator.py`) produces a realistic 10,000+ order dataset with:
- Correlated return rates by category (ethnic wear returns more than accessories)
- City-tier–aware logistics cost variation
- Seasonal demand patterns across 12 months
- Reproducible seed for consistent demos

### Robust Chart Guards
Every chart function handles edge cases explicitly:
```python
# size_heatmap_fig — 3-layer guard
if heatmap is None or heatmap.empty:         # Layer 1: empty check
    ...
try:
    pivot = heatmap.pivot_table(...)          # Layer 2: pivot try/catch
except (KeyError, ValueError):
    ...
if pivot.empty:                               # Layer 3: post-pivot check
    ...
```

### Theme-Aware Colorscales
Plotly colorscales use named built-ins (`"RdYlGn_r"`) rather than custom hex+alpha strings — avoiding validation errors in Python 3.14's stricter Plotly build.

---

## 🚀 Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/returniq-fashion-analytics.git
cd returniq-fashion-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

Sample data is auto-generated on first run — no external data source needed.

---

## 📋 Requirements

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
numpy>=1.26.0
```

---

## 🧩 SQL Query Pack (Included)

The `/sql/analysis_queries.sql` file ships with analyst-ready queries covering:

```sql
-- Which top revenue SKUs are net loss-makers?
-- Which size-category combinations drive the most return leakage?
-- How does Tier 2 profitability compare with Tier 1?
-- Which channel has the best profit per order after returns?
-- Which SKUs should merchandising prioritize before adding inventory?
-- What is the monthly trend in return-adjusted margin by category?
```

---

## 💡 Business Impact Framing

This dashboard is designed to answer questions that matter in real merchandising and e-commerce roles:

| Stakeholder | Question Answered |
|---|---|
| **Merchandising** | Which SKUs should we delist or reprice? |
| **Operations** | Which return reasons are costing us the most? |
| **Finance** | What is our actual margin after return economics? |
| **Growth** | Which city tier should we expand into next? |
| **Inventory** | Which SKUs carry triple-threat risk right now? |
| **CRM** | Are newer customer cohorts better or worse quality? |

---

## 👤 Author

Built by **AMRITA SINGH** as a portfolio project demonstrating:
- End-to-end Streamlit application architecture
- Domain expertise in Indian fashion e-commerce economics
- Data engineering (feature creation, synthetic data, KPI modelling)
- Production-grade error handling and defensive programming
- Full visual design system with dark/light theming

📧 amriiiita.07@email.com &nbsp;|&nbsp; 🔗 [LinkedIn] (www.linkedin.com/in/amriiiita07) 
&nbsp;|&nbsp; 🐙 [GitHub] (https://github.com/amriiiita07-ui)


