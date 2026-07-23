"""
Google Merchandise Store — Revenue & Funnel Analysis
======================================================
Full analysis code: SQL diagnostics (via BigQuery) + Python statistical validation.

Run in a Kaggle Notebook (free BigQuery public dataset access, no billing setup
needed) or any environment with `google-cloud-bigquery` configured.

Dataset : bigquery-public-data.ga4_obfuscated_sample_ecommerce
Scope   : Nov 1, 2020 - Jan 31, 2021 (3 months) | 267,116 sessions | $362,165 revenue
Author  : Chaitali Shashi Shekar
"""

from google.cloud import bigquery
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

client = bigquery.Client()
TABLE = "bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*"
DATE_RANGE = "_TABLE_SUFFIX BETWEEN '20201101' AND '20210131'"


# ======================================================================
# PHASE 1 — DATA EXPLORATION
# Business question: What events exist, and what does the schema look like?
# ======================================================================

Q1_EVENT_VOLUME = f"""
SELECT
  event_name,
  COUNT(*) AS event_count
FROM `{TABLE}`
WHERE {DATE_RANGE}
GROUP BY event_name
ORDER BY event_count DESC
"""

Q2_INSPECT_ECOMMERCE_STRUCTURE = """
SELECT ecommerce, items
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_20201101`
WHERE event_name = 'purchase'
LIMIT 1
"""


# ======================================================================
# PHASE 2 — FUNNEL DIAGNOSTICS
# Business question: Is the decline driven by traffic or conversion,
# and where in the funnel does it break down?
# ======================================================================

Q3_DAILY_REVENUE = f"""
SELECT
  event_date,
  COUNT(*) AS total_transactions,
  SUM(ecommerce.purchase_revenue) AS total_revenue,
  AVG(ecommerce.purchase_revenue) AS avg_order_value
FROM `{TABLE}`
WHERE {DATE_RANGE}
  AND event_name = 'purchase'
  AND ecommerce.purchase_revenue IS NOT NULL
GROUP BY event_date
ORDER BY event_date
"""

Q4_SESSIONS_VS_PURCHASERS = f"""
SELECT
  event_date,
  COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN user_pseudo_id END) AS sessions,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchasing_users
FROM `{TABLE}`
WHERE {DATE_RANGE}
GROUP BY event_date
ORDER BY event_date
"""

Q5_FULL_FUNNEL = f"""
SELECT
  COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN user_pseudo_id END) AS sessions,
  COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN user_pseudo_id END) AS viewed_item,
  COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) AS added_to_cart,
  COUNT(DISTINCT CASE WHEN event_name = 'begin_checkout' THEN user_pseudo_id END) AS began_checkout,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchased
FROM `{TABLE}`
WHERE {DATE_RANGE}
"""

Q6_FUNNEL_BY_MONTH = f"""
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
FROM `{TABLE}`
WHERE {DATE_RANGE}
GROUP BY month
"""


# ======================================================================
# PHASE 3 — SEGMENTATION
# Business question: Does the pattern vary by channel, device,
# geography, or customer type?
# ======================================================================

Q7_DEVICE_CHANNEL_JAN = """
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
"""

Q8_CHANNEL_TREND_3MO = f"""
SELECT
  CASE
    WHEN _TABLE_SUFFIX BETWEEN '20201101' AND '20201130' THEN 'November'
    WHEN _TABLE_SUFFIX BETWEEN '20201201' AND '20201231' THEN 'December'
    WHEN _TABLE_SUFFIX BETWEEN '20210101' AND '20210131' THEN 'January'
  END AS month,
  traffic_source.medium AS channel,
  COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN user_pseudo_id END) AS sessions,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchasers
FROM `{TABLE}`
WHERE {DATE_RANGE}
  AND traffic_source.medium IN ('cpc', 'organic', 'referral')
GROUP BY month, channel
ORDER BY month, channel
"""

Q9_NEW_VS_RETURNING = f"""
SELECT
  CASE
    WHEN user_first_touch_timestamp >= UNIX_MICROS(TIMESTAMP('2020-11-01'))
     AND user_first_touch_timestamp <= UNIX_MICROS(TIMESTAMP('2021-01-31 23:59:59'))
    THEN 'new_in_window'
    ELSE 'existing_before_window'
  END AS user_type,
  COUNT(DISTINCT user_pseudo_id) AS users,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchasers
FROM `{TABLE}`
WHERE {DATE_RANGE}
GROUP BY user_type
"""

Q10_REVENUE_BY_COUNTRY = f"""
SELECT
  geo.country,
  COUNT(DISTINCT CASE WHEN event_name = 'session_start' THEN user_pseudo_id END) AS sessions,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchasers,
  SUM(CASE WHEN event_name = 'purchase' THEN ecommerce.purchase_revenue ELSE 0 END) AS revenue
FROM `{TABLE}`
WHERE {DATE_RANGE}
GROUP BY geo.country
ORDER BY revenue DESC
LIMIT 15
"""

Q11_AOV_BY_DEVICE = f"""
SELECT
  device.category,
  COUNT(*) AS orders,
  SUM(ecommerce.purchase_revenue) AS revenue,
  AVG(ecommerce.purchase_revenue) AS aov
FROM `{TABLE}`
WHERE {DATE_RANGE}
  AND event_name = 'purchase'
  AND ecommerce.purchase_revenue IS NOT NULL
GROUP BY device.category
ORDER BY revenue DESC
"""


# ======================================================================
# PHASE 4 — STATISTICAL VALIDATION (Python)
# Business question: Is the observed decline statistically real, and
# is it isolated to one device/channel?
# ======================================================================

def run_ttest_dec_vs_jan(df_master: pd.DataFrame):
    """
    Independent (Welch's) t-test: December vs. January conversion rate.

    df_master must have columns: 'event_date' (datetime), 'conversion_rate'.

    Result obtained in this analysis: t = 4.332, p = 0.00006
    -> statistically significant (p < 0.001); the Dec-to-Jan decline is real,
       not random day-to-day noise.
    """
    dec_conv = df_master[df_master["event_date"].dt.month == 12].groupby("event_date")["conversion_rate"].mean()
    jan_conv = df_master[df_master["event_date"].dt.month == 1].groupby("event_date")["conversion_rate"].mean()
    t_stat, p_value = stats.ttest_ind(dec_conv, jan_conv, equal_var=False)
    return t_stat, p_value


def run_device_correlation(df_master: pd.DataFrame):
    """
    Pearson correlation between device-level daily conversion rates.

    df_master must have columns: 'event_date', 'device_category', 'conversion_rate'.

    Result obtained in this analysis: desktop-mobile r = 0.81 (strong).
    A shared movement across devices supports a seasonal/external cause
    rather than a device-specific bug.
    """
    pivot = df_master.groupby(["event_date", "device_category"])["conversion_rate"].mean().unstack()
    correlation_matrix = pivot.corr()
    return correlation_matrix


def run_revenue_forecast(daily_revenue: pd.DataFrame):
    """
    Simple linear trend forecast on daily revenue (and why it should NOT
    be trusted at face value).

    daily_revenue must have a 'revenue' column, one row per day, sorted by date.

    Result obtained in this analysis: slope = -44.27 revenue/day.
    Flagged as likely overstating the decline, since a straight line can't
    account for the Nov/Dec holiday spike that precedes it.
    """
    daily_revenue = daily_revenue.copy()
    daily_revenue["day_number"] = np.arange(len(daily_revenue))
    model = LinearRegression().fit(daily_revenue[["day_number"]], daily_revenue["revenue"])
    slope = model.coef_[0]
    return model, slope


# ======================================================================
# PHASE 5 — PRODUCT-LEVEL ANALYSIS
# Business question: Are any specific products underperforming, and why?
# ======================================================================

Q12_TOP_PRODUCTS = f"""
SELECT
  item.item_name,
  COUNT(DISTINCT CASE WHEN event_name = 'view_item' THEN user_pseudo_id END) AS viewers,
  COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) AS cart_adds,
  SUM(CASE WHEN event_name = 'purchase' THEN item.item_revenue ELSE 0 END) AS revenue
FROM `{TABLE}`,
UNNEST(items) AS item
WHERE {DATE_RANGE}
  AND event_name IN ('view_item', 'add_to_cart', 'purchase')
GROUP BY item.item_name
ORDER BY revenue DESC
LIMIT 20
"""

Q13_CART_ABANDONMENT_OVERALL = f"""
SELECT
  COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) AS added_to_cart_users,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchased_users
FROM `{TABLE}`
WHERE {DATE_RANGE}
"""

Q14_CART_ABANDONMENT_BY_PRODUCT = f"""
SELECT
  item.item_name,
  COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart' THEN user_pseudo_id END) AS added_to_cart,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' AND ecommerce.purchase_revenue IS NOT NULL THEN user_pseudo_id END) AS purchased
FROM `{TABLE}`,
UNNEST(items) AS item
WHERE {DATE_RANGE}
  AND event_name IN ('add_to_cart', 'purchase')
GROUP BY item.item_name
HAVING added_to_cart >= 100
ORDER BY added_to_cart DESC
LIMIT 20
"""


# ======================================================================
# RUN EXAMPLE (uncomment to execute in a Kaggle / BigQuery-enabled notebook)
# ======================================================================

if __name__ == "__main__":
    # Phase 1
    # df_events = client.query(Q1_EVENT_VOLUME).to_dataframe()

    # Phase 2
    # df_revenue = client.query(Q3_DAILY_REVENUE).to_dataframe()
    # df_funnel = client.query(Q5_FULL_FUNNEL).to_dataframe()

    # Phase 3
    # df_channel = client.query(Q8_CHANNEL_TREND_3MO).to_dataframe()

    # Phase 4 (requires df_master built from Phase 2/3 query results;
    # see README for exact column construction)
    # t_stat, p_value = run_ttest_dec_vs_jan(df_master)
    # corr_matrix = run_device_correlation(df_master)
    # model, slope = run_revenue_forecast(daily_revenue)

    # Phase 5
    # df_products = client.query(Q12_TOP_PRODUCTS).to_dataframe()

    print("Import this module's query strings and functions into a notebook "
          "with an authenticated BigQuery client to reproduce the analysis.")
