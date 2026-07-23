<div align="center">

# Google Merchandise Store: Diagnosing a Revenue Decline

*A business analytics case study using SQL, Python, Tableau, and product strategy.*
</div>

---

# Business Problem

Revenue is declining at the Google Merchandise Store, but traffic looks stable. That mismatch is what makes this worth investigating: if sessions aren't dropping, the leak is somewhere downstream, and "somewhere downstream" isn't a diagnosis leadership can act on.

---

# Dataset

| | |
|---|---|
| Dataset | Google Merchandise Store (GA4) |
| Time Period | Nov 2020 – Jan 2021 |
| Sessions | 267,116 |
| Revenue | $362,165 |

---

# Key Findings

| Finding |
|---------|
| Revenue decline was conversion-driven |
| Largest funnel leak occurred before checkout |
| Returning users converted 5.3× better |
| Conversion decline was statistically significant(p = 0.00006 ) |
| Desktop & Mobile followed the same seasonal trend(r = 0.81) |

---

# Executive Story

<table>
<tr>
<td><img src="assets/story/01_welcome.png" width="100%"></td>
<td><img src="assets/story/02_lone_climber.png" width="100%"></td>
<td><img src="assets/story/03_obstacle.png" width="100%"></td>
<td><img src="assets/story/04_investigation.png" width="100%"></td>
</tr>
<tr>
<td align="center"><sub>Welcome</sub></td>
<td align="center"><sub>The Journey Begins</sub></td>
<td align="center"><sub>The Obstacle</sub></td>
<td align="center"><sub>The Investigation</sub></td>
</tr>
<tr>
<td><img src="assets/story/05_solution.png" width="100%"></td>
<td><img src="assets/story/06_result.png" width="100%"></td>
<td><img src="assets/story/07_revenue.png" width="100%"></td>
<td></td>
</tr>
<tr>
<td align="center"><sub>The Solution</sub></td>
<td align="center"><sub>The Result</sub></td>
<td align="center"><sub>Business Impact</sub></td>
<td></td>
</tr>
</table>

---

# Live Dashboard

*(Insert Tableau preview here)*

---

# Repository Guide

| Folder | Description |
|---------|-------------|
| `/sql` | BigQuery SQL analysis |
| `/python` | Statistical analysis |
| `/dashboard` | Tableau dashboard |
| `/product-solution` | Product proposal |
| `/presentation` | Executive presentation |
| `/docs` | Methodology and formulas |

---

# Technologies

- SQL (BigQuery)
- Python
- Tableau
- Figma
- Google Analytics 4
