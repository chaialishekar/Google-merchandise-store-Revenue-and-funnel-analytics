<div align="center">

# 📊 Google Merchandise Store: Revenue & Funnel Analysis

**Diagnosing revenue loss in a real e-commerce funnel — validated statistically, resolved into a product solution.**

[![SQL](https://img.shields.io/badge/SQL-BigQuery-4285F4?style=flat-square&logo=googlebigquery&logoColor=white)](https://cloud.google.com/bigquery)
[![Python](https://img.shields.io/badge/Python-pandas%20%7C%20scipy%20%7C%20sklearn-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Tableau](https://img.shields.io/badge/Tableau-Public-E97627?style=flat-square&logo=tableau&logoColor=white)](https://public.tableau.com/views/G4RevenueAnalytics/Dashboard2)
[![Figma](https://img.shields.io/badge/Figma-Wireframes-F24E1E?style=flat-square&logo=figma&logoColor=white)](#)

[The Story](#-the-story) · [Live Dashboard](#-live-interactive-dashboard) · [Key Findings](#-key-findings) · [Code & Analysis](#-code--statistical-analysis) · [Formulas](#-statistical-formulas) · [Deliverables](#-deliverables)

</div>

---

## Overview

Leadership noticed fluctuating traffic and revenue at the Google Merchandise Store and needed to know: **is this a traffic problem or a conversion problem, where exactly does the funnel break down, and is it structural or seasonal?**

Using 267,116 sessions of GA4 event-level data (BigQuery), this project answers all three — with SQL diagnostics, statistical validation, and a behavioral product solution proposed in response.

| | |
|---|---|
| **Dataset** | [`bigquery-public-data.ga4_obfuscated_sample_ecommerce`](https://console.cloud.google.com/bigquery) |
| **Scope** | Nov 1, 2020 – Jan 31, 2021 · 267,116 sessions · $362,165 revenue |
| **Skills** | SQL (BigQuery), hypothesis testing, correlation analysis, funnel/cohort analysis, product strategy |

---

## 🥾 The Story

<table>
<tr>
<td width="25%"><img src="story_images/01_welcome.png" width="100%"/></td>
<td width="25%"><img src="story_images/02_lone_climber.png" width="100%"/></td>
<td width="25%"><img src="story_images/03_obstacle.png" width="100%"/></td>
<td width="25%"><img src="story_images/04_investigated.png" width="100%"/></td>
</tr>
<tr>
<td align="center"><sub><b>1.</b> The setup</sub></td>
<td align="center"><sub><b>2.</b> The climb begins</sub></td>
<td align="center"><sub><b>3.</b> The obstacle</sub></td>
<td align="center"><sub><b>4.</b> The investigation</sub></td>
</tr>
<tr>
<td width="25%"><img src="story_images/05_solution_bridge.png" width="100%"/></td>
<td width="25%"><img src="story_images/06_summit.png" width="100%"/></td>
<td width="25%"><img src="story_images/07_revenue.png" width="100%"/></td>
<td width="25%"></td>
</tr>
<tr>
<td align="center"><sub><b>5.</b> The solution</sub></td>
<td align="center"><sub><b>6.</b> The result</sub></td>
<td align="center"><sub><b>7.</b> The payoff</sub></td>
<td></td>
</tr>
</table>

*A visitor is a hiker climbing toward checkout. Most hit an obstacle and turn back — this project investigates why, and builds the bridge that gets more of them to the top.*

---

## 📺 Live Interactive Dashboard

[![Dashboard Preview](https://public.tableau.com/static/images/G4/G4RevenueAnalytics/Dashboard2/1.png)](https://public.tableau.com/views/G4RevenueAnalytics/Dashboard2)

**[→ Open the live dashboard on Tableau Public](https://public.tableau.com/views/G4RevenueAnalytics/Dashboard2)** — filter by month, channel, and device directly.

---

## 🔍 Key Findings

| # | Finding | Evidence |
|---|---|---|
| 1 | Revenue decline is **conversion-driven**, not traffic-driven | Sessions held flat (~2,300–4,600/day); conversion fell 1.73% → 0.89% (Dec→Jan) |
| 2 | The funnel's largest leak is **before checkout** | Only 23% of sessions view a product; checkout-to-purchase is a healthy 42% |
| 3 | The decline is **statistically significant** | t = 4.332, p = 0.00006 |
| 4 | The decline is **seasonal**, not a broken feature | Desktop/mobile conversion correlate at r = 0.81 |
| 5 | **Paid traffic underperforms** free traffic, every month | CPC converts lowest of all channels, Nov–Jan without exception |
| 6 | **Returning customers convert 5.3x better** | 6.67% vs. 1.25% conversion |
| 7 | Geography & device **don't** explain the pattern | Conversion uniform ~1.2–1.9%; AOV flat ~$67–70 |
| 8 | Cart abandonment (67.6%) is **industry-normal** | Typical benchmark is ~70% — no urgent fix needed |

---

## 💻 Code & Statistical Analysis

All SQL queries and Python statistical code live in a single file:

### **[`analysis.py`](./analysis.py)**

| Section | Business Question |
|---|---|
| Phase 1 — Data Exploration | What events exist? What's the schema? |
| Phase 2 — Funnel Diagnostics | Traffic or conversion problem? Where's the drop-off? |
| Phase 3 — Segmentation | Does it vary by channel, device, geography, or user type? |
| Phase 4 — Statistical Validation | Is the decline real? Isolated to one segment? |
| Phase 5 — Product-Level Analysis | Are specific products underperforming? |

Each query/function is documented inline with the business question it answers and the exact result obtained in this analysis.

**Known data caveats**, identified and handled in the code:
- `transaction_id` is frequently null on `purchase` events → revenue queries filter on `ecommerce.purchase_revenue IS NOT NULL` instead
- `traffic_source.medium` occasionally shows `(data deleted)` (a GA4 privacy redaction) → excluded from channel-level conclusions
- November shows `add_to_cart` counts lower than `begin_checkout` counts in aggregate → flagged as a likely non-cart checkout path, not a real >100% conversion

**To run it:** open a free [Kaggle](https://kaggle.com) Notebook (BigQuery public dataset access is pre-configured, no billing needed), upload `analysis.py`, and import the query strings / functions you need.

---

## 📐 Statistical Formulas

The core metrics and tests referenced in `analysis.py`:

**Conversion Rate**
```math
CR = \frac{\text{Purchasers}}{\text{Sessions}} \times 100
```

**Average Order Value (AOV)**
```math
AOV = \frac{\text{Total Revenue}}{\text{Number of Transactions}}
```

**Cart Abandonment Rate**
```math
CAR = 1 - \frac{\text{Purchased Users}}{\text{Added-to-Cart Users}}
```

**Welch's t-test** — tested whether the Dec → Jan conversion drop was statistically real
```math
t = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\dfrac{s_1^2}{n_1} + \dfrac{s_2^2}{n_2}}}
```
Result: t = 4.332, p = 0.00006 — far below the 0.05 significance threshold.

**Pearson Correlation Coefficient** — tested whether desktop/mobile moved together
```math
r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}
```
Result: r = 0.81 (strong positive correlation).

**Simple Linear Regression** — used for the revenue trend forecast
```math
\hat{y} = \beta_0 + \beta_1 x, \qquad \beta_1 = \frac{\sum (x_i-\bar{x})(y_i-\bar{y})}{\sum(x_i-\bar{x})^2}
```
Result: slope β₁ = -44.27 revenue/day — flagged as likely overstating the decline (can't account for the Nov/Dec holiday spike).

---

## 📂 Repository Structure

```
├── README.md
├── analysis.py              ← all SQL queries + Python statistical code
├── story_images/            ← the 7 story panels shown above
└── deliverables/
    ├── GA4_Full_Presentation.pptx
    ├── GA4_Discovery_Assistant_Proposal.pdf
    ├── GA4_Revenue_Funnel_GTM_Strategy.pptx
    ├── GA4_Revenue_to_Solution_Overview.pptx
    └── GA4_Business_Summary.pdf
```

---

## 📦 Deliverables

| File | Description |
|---|---|
| `GA4_Full_Presentation.pptx` | Complete deck: problem → analysis → solution → personas → wireframes → forecast → success metrics |
| `GA4_Discovery_Assistant_Proposal.pdf` | Three-part report: diagnosis → behavioral product solution → GTM strategy |
| `GA4_Revenue_Funnel_GTM_Strategy.pptx` | Full findings + GTM strategy deck |
| `GA4_Revenue_to_Solution_Overview.pptx` | Condensed 8-slide summary |
| `GA4_Business_Summary.pdf` | 3-page executive summary |

---

<div align="center">

*Analysis performed using Google BigQuery (SQL), Python (pandas, scipy, scikit-learn), and Tableau/Figma for visualization.*

</div>
