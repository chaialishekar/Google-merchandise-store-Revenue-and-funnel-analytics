<div align="center">

# 📊 Google Merchandise Store: Diagnosing a Revenue Decline

**A data-driven investigation into declining e-commerce revenue using SQL, Python, Tableau, and product strategy.**

[![SQL](https://img.shields.io/badge/SQL-BigQuery-4285F4?style=flat-square&logo=googlebigquery&logoColor=white)](https://cloud.google.com/bigquery)
[![Python](https://img.shields.io/badge/Python-pandas%20%7C%20scipy%20%7C%20sklearn-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Tableau](https://img.shields.io/badge/Tableau-Public-E97627?style=flat-square&logo=tableau&logoColor=white)](https://public.tableau.com/)
[![Figma](https://img.shields.io/badge/Figma-Wireframes-F24E1E?style=flat-square&logo=figma&logoColor=white)](#)

[Live Dashboard](#-live-dashboard) •
[Key Findings](#-key-findings) •
[Repository Guide](#-repository-guide)

</div>

---

# Business Problem

Leadership observed declining revenue in the Google Merchandise Store despite relatively stable website traffic.

The objective of this project was to determine:

- Is revenue loss caused by fewer visitors or lower conversion?
- Where does the purchase funnel break down?
- Is the decline statistically significant?
- What product improvements could increase conversions?

Using Google Analytics 4 event-level data from BigQuery, this project combines SQL, statistical analysis, visualization, and product thinking to answer these questions.

---

# Dataset

| | |
|---|---|
| Dataset | Google Merchandise Store (GA4 Sample) |
| Time Period | Nov 2020 – Jan 2021 |
| Sessions | 267,116 |
| Revenue | $362,165 |
| Source | BigQuery Public Dataset |

---

# Analysis Workflow

```text
GA4 Event Data
       │
       ▼
SQL Funnel Analysis
       │
       ▼
Customer Segmentation
       │
       ▼
Statistical Validation
       │
       ▼
Business Insights
       │
       ▼
Product Recommendation
```

---

# Key Findings

| Finding | Result |
|---------|--------|
| Revenue decline was conversion-driven | ✅ |
| Largest funnel drop occurred before checkout | ✅ |
| Conversion decline was statistically significant | p = 0.00006 |
| Desktop & Mobile followed the same seasonal trend | r = 0.81 |
| Returning users converted 5.3× better | ✅ |
| Paid traffic consistently underperformed organic traffic | ✅ |

---

# Live Dashboard

[![Dashboard Preview](dashboard/dashboard_preview.png)](https://public.tableau.com/views/G4RevenueAnalytics/Dashboard2)

**Explore the interactive Tableau dashboard** to filter revenue, conversion, channel, device, and customer segments.

---

# Repository Guide

| Folder | Contents |
|---------|----------|
| `/sql` | BigQuery SQL queries used throughout the analysis |
| `/python` | Statistical tests, forecasting, and supporting analysis |
| `/dashboard` | Tableau workbook and dashboard preview |
| `/product-solution` | Product proposal, wireframes, and GTM strategy |
| `/presentations` | Executive presentation and full case study |
| `/docs` | Methodology, assumptions, and statistical notes |

---

# Project Structure

```text
.
├── README.md
├── sql/
├── python/
├── dashboard/
├── product-solution/
├── presentations/
├── docs/
└── assets/
```

---

# Technologies

- SQL (Google BigQuery)
- Python (Pandas, SciPy, Scikit-learn)
- Tableau
- Figma
- Google Analytics 4

---

# Highlights

- Diagnosed the root cause of declining revenue using event-level GA4 data
- Built SQL funnel and customer segmentation analyses
- Validated findings using hypothesis testing and correlation analysis
- Developed a product recommendation supported by user behavior
- Communicated findings through an executive dashboard and presentation

---

# Additional Resources

📊 **Dashboard**

- Tableau Public Dashboard

📈 **SQL Analysis**

- `/sql`

📉 **Statistical Analysis**

- `/python`

💡 **Product Proposal**

- `/product-solution`

📑 **Executive Presentation**

- `/presentations`

---

<div align="center">

**From business problem → analytics → statistical validation → product recommendation**

</div>
