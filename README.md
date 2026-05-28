# 🏦 European Bank — Customer Engagement & Retention Analytics

> **Live Dashboard →** *(add your Streamlit Cloud URL here after deployment)*

A behavioral churn analysis dashboard for European banking customers, built for the **European Central Bank's Customer Behavior Analytics Division**.

---

## 📊 Dashboard Overview

This Streamlit app provides four interactive analytics modules across 10,000 customer records from France, Germany, and Spain:

| Tab | Description |
|-----|-------------|
| 📊 **Engagement Overview** | Active vs inactive churn, geography, age cohort, tenure, gender breakdowns |
| 📦 **Product Utilization** | Churn by product count, activity × product heatmap, balance tier analysis |
| 🔍 **High-Value Detector** | Identifies retained high-balance inactive customers at risk of silent churn |
| 🧮 **Retention Strength** | Relationship Strength Index (RSI) scoring, sticky customer profiling |

### Sidebar Filters (applied across all charts)
- 🌍 Geography (France / Germany / Spain)
- 👤 Gender
- 📦 Product count range
- 💰 Balance & salary thresholds
- 🎯 Activity status (Active / Inactive)
- 📅 Tenure range

---

## 🔑 Key Findings

| Insight | Value |
|---------|-------|
| Overall churn rate | **20.4%** |
| Active member churn | **14.3%** vs 26.9% inactive |
| 1 → 2 product churn reduction | **−20.1 percentage points** |
| Germany churn anomaly | **32.4%** (2× France & Spain) |
| Age 51–60 churn rate | **56.2%** — highest cohort |
| High-value silent churn risk | **32.8%** (balance > €100k, inactive) |
| RSI discriminatory power | **2.85×** (Low vs High RSI) |

---

## 🚀 Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/european-bank-retention.git
cd european-bank-retention

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py
```

Make sure `European_Bank.csv` is in the same directory as `app.py`.

---

## 📁 Repository Structure

```
european-bank-retention/
├── app.py                          # Main Streamlit dashboard
├── European_Bank.csv               # Dataset (10,000 customers)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 📐 Methodology

### Engagement Tier Classification
Customers segmented by activity status × product count into four tiers ranging from **Active Multi-product** (9.7% churn) to **Inactive Single-product** (36.7% churn).

### Relationship Strength Index (RSI)
Composite behavioral score (0–120):

```
RSI = IsActiveMember × 40
    + min(NumOfProducts, 2) × 20
    + HasCrCard × 10
    + min(Tenure, 10) × 3
```

**RSI Tiers:** Low (< 50) → 35.3% churn | Medium (50–79) → 20.8% | High (≥ 80) → 12.4%

---

## 🏛️ Context

This project reframes customer churn from a **behavioral and relationship-strength perspective**. By focusing on engagement and product utilization rather than demographics, it provides actionable insights for:
- Cross-sell strategy design
- Loyalty programme targeting
- Silent premium churn prevention
- CRM early-warning systems

---

## 📄 License

For academic and government analytics use. Dataset sourced from European Bank Customer records, 2025.
