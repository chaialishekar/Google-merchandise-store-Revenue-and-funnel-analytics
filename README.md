# Google Merchandise Store: Revenue & Funnel Analysis

Revenue and conversion analysis of the Google Merchandise Store using Google Analytics 4 (GA4) event-level data. Built to diagnose *where* revenue is being lost in the purchase funnel, confirm findings statistically, and translate them into a prioritized business recommendation.

**Skills demonstrated:** SQL (BigQuery), statistical hypothesis testing, correlation analysis, funnel/cohort analysis, business recommendation.

---

## Table of Contents

- [Business Problem](#business-problem)
- [Dataset](#dataset)
- [Repository Structure](#repository-structure)
- [Key Findings](#key-findings)
- [Queries by Phase](#queries-by-phase)
  - [Phase 1 — Data Exploration](#phase-1--data-exploration)
  - [Phase 2 — Funnel Diagnostics](#phase-2--funnel-diagnostics)
  - [Phase 3 — Segmentation](#phase-3--segmentation)
  - [Phase 4 — Statistical Validation (Python)](#phase-4--statistical-validation-python)
  - [Phase 5 — Product-Level Analysis](#phase-5--product-level-analysis)
  - [Phase 6 — Tableu live Dashboard](#phase-6--Tableu-Dashboard)
- [How to Reproduce](#how-to-reproduce)
- [Deliverables](#deliverables)

---

## Business Problem

Leadership observed fluctuating traffic and revenue and wanted to understand user behavior across the purchase funnel, identify where conversion breaks down, and get data-backed recommendations to grow revenue.

This analysis answers three questions:
1. Is the revenue decline a traffic problem or a conversion problem?
2. Where exactly in the funnel are customers dropping off?
3. Is the decline a real, structural issue or normal seasonal variation?

## Dataset

| | |
|---|---|
| **Source** | [`bigquery-public-data.ga4_obfuscated_sample_ecommerce`](https://console.cloud.google.com/bigquery) (BigQuery Public Datasets) |
| **Company** | Google Merchandise Store (Google-branded apparel/accessories) |
| **Date range** | November 1, 2020 – January 31, 2021 (3 months) |

## Repository Structure

```
├── README.md                     ← you are here
├── 01_data_exploration/          ← schema discovery, event inventory
├── 02_funnel_diagnostics/        ← core funnel + traffic vs. conversion queries
├── 03_segmentation/              ← channel, device, geography, new vs. returning
├── 04_statistical_validation/    ← t-test, correlation, forecast (Python)
├── 05_product_analysis/          ← product-level revenue and cart abandonment
└── deliverables/
    ├── GA4_Revenue_Funnel_GTM_Strategy.pptx
    ├── GA4_Discovery_Assistant_Proposal.pdf
    └── GA4_Revenue_to_Solution_Overview.pptx
```

## Key Findings

| # | Finding | Evidence |
|---|---|---|
| 1 | Revenue decline is a **conversion problem**, not a traffic problem | Sessions held flat (~2,300–4,600/day); conversion fell from 1.73% (Dec) to 0.89% (Jan) |
| 2 | The funnel's largest leak is **before checkout**, not during it | Only 23% of sessions view a product; checkout-to-purchase is a healthy 42% |
| 3 | The decline is **statistically significant** | t = 4.332, p = 0.00006 (Dec vs. Jan conversion rate) |
| 4 | The decline is **seasonal**, not a broken feature | Desktop/mobile conversion correlate at r = 0.81 — a shared cause, not a device-specific bug |
| 5 | **Paid traffic underperforms free traffic**, every month | CPC converts lowest of all channels in Nov, Dec, and Jan without exception |
| 6 | **Returning customers convert 5.3x better** than new customers | 6.67% vs. 1.25% conversion |
| 7 | Geography and device **don't** explain the pattern | Conversion uniform ~1.2–1.9% across countries; AOV flat ~$67–70 across devices |
| 8 | Cart abandonment (67.6%) is **in line with industry norms** (~70%) | No urgent fix needed here |

---

## Queries by Phase

### Phase 1 — Data Exploration

**Business question:** What events exist, and what does the schema look like?

```sql
-- Event volume by type
SELECT
  event_name,
  COUNT(*) AS event_count
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
GROUP BY event_name
ORDER BY event_count DESC
```

```sql
-- Inspect nested ecommerce/items structure on a real purchase record
SELECT ecommerce, items
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_20201101`
WHERE event_name = 'purchase'
LIMIT 1
```

### Phase 2 — Funnel Diagnostics

**Business question:** Is the decline driven by traffic or conversion, and where in the funnel does it break down?

```sql
-- Daily revenue, filtered to valid (non-null) purchases
SELECT
  event_date,
  COUNT(*) AS total_transactions,
  SUM(ecommerce.purchase_revenue) AS total_revenue,
  AVG(ecommerce.purchase_revenue) AS avg_order_value
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
  AND event_name = 'purchase'
  AND ecommerce.purchase_revenue IS NOT NULL
GROUP BY event_date
ORDER BY event_date
```

```sql
-- Sessions vs. purchasing users, to isolate traffic from conversion
SELECT
  event_date,
  COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN user_pseudo_id END) AS sessions,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchasing_users
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
GROUP BY event_date
ORDER BY event_date
```

```sql
-- Full funnel: Sessions → Viewed → Cart → Checkout → Purchased
SELECT
  COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN user_pseudo_id END) AS sessions,
  COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN user_pseudo_id END) AS viewed_item,
  COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) AS added_to_cart,
  COUNT(DISTINCT CASE WHEN event_name = 'begin_checkout' THEN user_pseudo_id END) AS began_checkout,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchased
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
```

```sql
-- Funnel by month, to test the seasonality hypothesis
SELECT
  CASE
    WHEN _TABLE_SUFFIX BETWEEN '20201101' AND '20201130' THEN 'November'
    WHEN _TABLE_SUFFIX BETWEEN '20201201' AND '20201231' THEN 'December'
    WHEN _TABLE_SUFFIX BETWEEN '20210101' AND '20210131' THEN 'January'
  END AS month,
  COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN user_pseudo_id END) AS viewed_item,
  COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) AS added_to_cart,
  COUNT(DISTINCT CASE WHEN event_name = 'begin_checkout' THEN user_pseudo_id END) AS began_checkout,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchased
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
GROUP BY month
```

### Phase 3 — Segmentation

**Business question:** Does the pattern vary by channel, device, geography, or customer type?

```sql
-- Device × channel breakdown, January
SELECT
  device.category AS device_category,
  traffic_source.medium AS channel,
  COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN user_pseudo_id END) AS sessions,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchasers,
  SUM(CASE WHEN event_name = 'purchase' THEN ecommerce.purchase_revenue ELSE 0 END) AS revenue
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20210101' AND '20210131'
GROUP BY device_category, channel
ORDER BY revenue DESC
```

```sql
-- Channel conversion trend across all 3 months (CPC vs. Organic vs. Referral)
SELECT
  CASE
    WHEN _TABLE_SUFFIX BETWEEN '20201101' AND '20201130' THEN 'November'
    WHEN _TABLE_SUFFIX BETWEEN '20201201' AND '20201231' THEN 'December'
    WHEN _TABLE_SUFFIX BETWEEN '20210101' AND '20210131' THEN 'January'
  END AS month,
  traffic_source.medium AS channel,
  COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN user_pseudo_id END) AS sessions,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchasers
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
  AND traffic_source.medium IN ('cpc', 'organic', 'referral')
GROUP BY month, channel
ORDER BY month, channel
```

```sql
-- New vs. returning user conversion
SELECT
  CASE
    WHEN user_first_touch_timestamp >= UNIX_MICROS(TIMESTAMP('2020-11-01'))
     AND user_first_touch_timestamp <= UNIX_MICROS(TIMESTAMP('2021-01-31 23:59:59'))
    THEN 'new_in_window'
    ELSE 'existing_before_window'
  END AS user_type,
  COUNT(DISTINCT user_pseudo_id) AS users,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchasers
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
GROUP BY user_type
```

```sql
-- Revenue and conversion by country
SELECT
  geo.country,
  COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN user_pseudo_id END) AS sessions,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchasers,
  SUM(CASE WHEN event_name = 'purchase' THEN ecommerce.purchase_revenue ELSE 0 END) AS revenue
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
GROUP BY geo.country
ORDER BY revenue DESC
LIMIT 15
```

```sql
-- Average order value by device
SELECT
  device.category,
  COUNT(*) AS orders,
  SUM(ecommerce.purchase_revenue) AS revenue,
  AVG(ecommerce.purchase_revenue) AS aov
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
  AND event_name = 'purchase'
  AND ecommerce.purchase_revenue IS NOT NULL
GROUP BY device.category
ORDER BY revenue DESC
```

### Phase 4 — Statistical Validation (Python)

**Business question:** Is the observed decline statistically real, and is it isolated to one device/channel?

```python
# Independent t-test: December vs. January conversion rate
from scipy import stats

dec_conv = df_master[df_master['event_date'].dt.month == 12].groupby('event_date')['conversion_rate'].mean()
jan_conv = df_master[df_master['event_date'].dt.month == 1].groupby('event_date')['conversion_rate'].mean()

t_stat, p_value = stats.ttest_ind(dec_conv, jan_conv, equal_var=False)
# Result: t = 4.332, p = 0.00006 → statistically significant
```

```python
# Correlation between device conversion rates, to test the seasonality hypothesis
pivot = df_master.groupby(['event_date', 'device_category'])['conversion_rate'].mean().unstack()
correlation_matrix = pivot.corr()
# Result: desktop–mobile r = 0.81 (strong) → supports a shared external cause
```

```python
# Simple linear trend forecast (and why it should NOT be trusted at face value)
import numpy as np
from sklearn.linear_model import LinearRegression

daily_revenue['day_number'] = np.arange(len(daily_revenue))
model = LinearRegression().fit(daily_revenue[['day_number']], daily_revenue['revenue'])
# Result: slope = -44.27/day. Flagged as likely overstating the decline,
# since a straight line can't account for the Nov/Dec holiday spike.
```

### Phase 5 — Product-Level Analysis

**Business question:** Are any specific products underperforming, and why?

```sql
-- Top products by revenue, with view-to-cart rate
SELECT
  item.item_name,
  COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN user_pseudo_id END) AS viewers,
  COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) AS cart_adds,
  SUM(CASE WHEN event_name = 'purchase' THEN item.item_revenue ELSE 0 END) AS revenue
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`,
UNNEST(items) AS item
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
  AND event_name IN ('view_item', 'add_to_cart', 'purchase')
GROUP BY item.item_name
ORDER BY revenue DESC
LIMIT 20
```

```sql
-- Overall cart abandonment rate
SELECT
  COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) AS added_to_cart_users,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchased_users
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
```

```sql
-- Cart abandonment by individual product
SELECT
  item.item_name,
  COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) AS added_to_cart,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchased
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`,
UNNEST(items) AS item
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
  AND event_name IN ('add_to_cart', 'purchase')
GROUP BY item.item_name
HAVING added_to_cart >= 100
ORDER BY added_to_cart DESC
LIMIT 20
```

---


## Phase 6 — Tableu Dashboard

| DASHBOARD |
|---|
|[Full findings: DASHBOARD ](https://public.tableau.com/views/G4RevenueAnalytics/Dashboard2?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) |

<div class='tableauPlaceholder' id='viz1784772223725' style='position: relative'><noscript><a href='#'><img alt='Dashboard 2 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;G4&#47;G4RevenueAnalytics&#47;Dashboard2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='G4RevenueAnalytics&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;G4&#47;G4RevenueAnalytics&#47;Dashboard2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1784772223725');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else { vizElement.style.width='100%';vizElement.style.height='1527px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>

## RECOMMENDATIONS 
| FILE | DESCRIPTION
|---|---|
| `GA4_Discovery_Assistant_Proposal.pdf` | Three-part report: diagnosis → behavioral product solution → GTM strategy |
| `GA4_Revenue_to_Solution_Overview.pptx` | Condensed 8-slide summary deck |

---

*Analysis performed using Google BigQuery (SQL), Python (pandas, scipy, scikit-learn), and Tableau/Figma for visualization.*
