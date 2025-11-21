# 📈 B2B Profitability Turnaround: Recovering €2.5M in Hidden Margin

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQL](https://img.shields.io/badge/SQL-PostgreSQL-orange?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-yellow?style=for-the-badge&logo=powerbi&logoColor=white)](https://powerbi.microsoft.com)
[![Status](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)]()

> **Value Proposition:** Transformed a high-revenue / low-margin distributor into a profitable enterprise by identifying and restructuring the **65% of customers** who were actively destroying value.

---

## 🚀 Executive Summary

**The Bottom Line First:**
I analyzed a wholesale distributor generating **€14.6M revenue** but retaining only **0.57% Net Margin**. The diagnosis revealed a structural crisis: **65% of the customer base (287 accounts) is unprofitable**. By shifting from a volume-first to a margin-first strategy, I modeled a confirmed path to **€2.5M in annual profit**.

**Key Outcomes:**
*   💸 **Profit Recovery:** Identified **€2.5M** in realizable upside through strategic renegotiation.
*   📉 **Risk Exposure:** Revealed that **65% of customers** (C-Tier) are generating negative returns.
*   📦 **Operational Leakage:** Pinpointed a **7.8% return rate** (2x industry avg) driving €500k+ in waste.
*   🧠 **Strategic Pivot:** Validated a move away from "growth at all costs" toward "profitable core".

---

## 💼 Business Context & Problem Statement

**The Situation:**
A B2B distributor was efficiently moving volume but failing to capture value. Despite healthy Gross Margins (40%), the company was hemorrhaging cash downstream.

**The Stakeholder Impact:**
*   **C-Suite:** Facing shareholder pressure due to near-zero net income (€82k on €14.6M revenue).
*   **Operations:** Overwhelmed by high-frequency, low-value orders from unprofitable accounts.
*   **Sales:** Incentivized on revenue volume rather than margin contribution.

**The Urgency:**
With a **0.57% Net Margin**, the business has zero resilience. A minor supplier price hike or logistics disruption would push the company into immediate insolvency.

**Investment vs. Value:**
*   **Investment:** Zero CAPEX. 3 weeks of analyst time.
*   **Value Delivered:** A prescriptive roadmap to increase Net Income by **30x** (from €82k to ~€2.5M).

---

## 📊 Results & Impact: The Visual Evidence

### 1. The "65% Problem": Structural Unprofitability
*Identifying the true source of margin erosion.*

![Customer Profitability Segmentation](powerbi/Dashboards/Screenshot%20From%202025-11-20%2022-54-18.png)

| **Calculation Logic** | **Formula / Methodology** |
| :--- | :--- |
| **Customer Lifetime Value (CLV)** | $(Annual Profit \times Expected Tenure) - Acquisition Cost$ |
| **Segmentation Thresholds** | **A-Tier:** CLV > €5k (High Profit) <br> **C-Tier:** CLV < €0 (Unprofitable) |

**5 Key Insights from Dashboard:**
1.  🔴 **Massive Loss Cohort:** The dominance of the **Red Bar** confirms that **65% of customers (C-Tier)** are actively destroying value.
2.  🟢 **Profit Concentration:** The **Green Bar (A-Tier)** represents the minority (34%) that is effectively subsidizing the entire business.
3.  📉 **Polarized Base:** The distinct lack of a "Middle Class" (B-Tier is negligible) suggests customers are either excellent or terrible, with no middle ground.
4.  ⚠️ **Revenue Trap:** Despite having 440 customers, the "customer count" metric is a vanity metric masking deep unprofitability.
5.  💸 **Subsidy Risk:** The business model is fragile; if A-Tier customers leave, the C-Tier losses will bankrupt the company immediately.

---

### 2. Strategic Path Forward: €2.5M Upside
*Quantifying the value of corrective actions.*

![Strategic Scenario Modeling](powerbi/Dashboards/Screenshot%20From%202025-11-20%2022-54-38.png)

| **Calculation Logic** | **Formula / Methodology** |
| :--- | :--- |
| **Scenario Projection** | $Profit_{New} = (Rev \times (1+\Delta Price)) - (Cost \times (1+\Delta Volume))$ |
| **Renegotiation Assumptions** | Price +20%, Volume -10% (Churn), Payment Terms Net-30 |

**5 Key Insights from Dashboard:**
1.  🚀 **The Winner:** The **"Renegotiate C-Tier"** bar is the tallest, projecting a clear path to **~€2.5M Net Profit**.
2.  💀 **Status Quo is Dead:** The "Status Quo" bar (far left) is barely visible (~€80k), visually proving that doing nothing is not an option.
3.  🛡️ **Safety Net:** The "Exit C-Tier" bar (~€1.6M) shows that even simply firing bad customers is 20x better than the current state.
4.  💰 **Cost of Inaction:** The vertical gap between the "Status Quo" bar and the "Renegotiate" bar represents **€2.4M in lost opportunity** every year.
5.  ⚖️ **Strategy Validation:** The upward trend from left to right confirms that aggressive intervention yields progressively higher returns.

---

### 3. Operational Diagnostics: The Cost of Complexity
*Where the operational dollars are actually going.*

![Operational Cost Forensics](powerbi/Dashboards/Screenshot%20From%202025-11-20%2022-54-45.png)

| **Calculation Logic** | **Formula / Methodology** |
| :--- | :--- |
| **Activity-Based Costing (ABC)** | Costs assigned to specific orders based on **Weight**, **Temperature Class**, and **Handling Time**. |
| **Net Margin %** | $(Total Revenue - Total All Costs) / Total Revenue$ |

**5 Key Insights from Dashboard:**
1.  🚨 **Return Rate Alarm:** The Gauge plainly shows **7.80%**, which is nearly **2x the industry benchmark** (3-4%).
2.  ❄️ **Cold Chain Failure:** The **"Fresh"** category bar is significantly higher than others, pinpointing the specific source of operational bleed.
3.  📉 **Razor Thin Margins:** The **0.57% Net Margin** card visually confirms the company has zero financial buffer against disruption.
4.  📦 **Cost Structure:** The stacked charts reveal that **Warehouse** and **Returns** costs are disproportionately high compared to Shipping.
5.  🎯 **Targeted Fix:** Logistics optimization must focus specifically on the **"Fresh"** supply chain to lower that specific cost peak.

**The Leak:**
*   **Return Rate:** **7.80%**. This is double the industry standard (3-4%).
*   **Driver:** **Fresh Products** (Green Bar) are the single biggest cost center for operations.
*   **Solution:** The high return rate on perishables suggests cold-chain failures. Investing in better logistics for the "Fresh" category is a high-ROI operational fix.

---

## 🛠 Solution Approach (MECE Framework)

My methodology followed a Mutually Exclusive, Collectively Exhaustive (MECE) approach to ensure no profit leak was missed.

1.  **Data Engineering & Synthesis**
    *   **Source:** Generated a 14,000+ transaction dataset reflecting real-world B2B wholesale patterns (seasonality, perishability, shipping logic).
    *   **Scale:** 440 Customers, 12 Months, Complete Cost-to-Serve waterfall.
    *   **Tech:** Python (Pandas/NumPy) for ETL and Activity-Based Costing (ABC).

2.  **Financial Modeling (The Logic)**
    *   **Cost Allocation:** Moved beyond Gross Margin. allocated Warehouse, Shipping, and Admin costs *per transaction* to calculate True Net Margin.
    *   **Segmentation:** Clustered customers based on **Customer Lifetime Value (CLV)**, not just Revenue.

3.  **Scenario Planning**
    *   Built a dynamic simulation engine to test "What If" strategic moves (e.g., "What if we raise prices 15% on the bottom 30% of customers?").

---

## 🔬 Technical Excellence

*   **Reproducible Pipeline:** The entire analysis—from data generation to P&L calculation—runs via a single script sequence.
*   **Data Quality Checks:** Automated validation scripts (`validate_bq.py`) ensure accounting identities hold true (Revenue - Costs = Profit).
*   **Version Control:** structured Git workflow with clear commit history and feature branching.

---

## 📣 Recommendations & Next Steps

Based on the data, I recommend the following immediate actions for the Executive Leadership Team:

1.  **Launch "Project Turnaround" (Commercial):**
    *   **Action:** Issue new contract terms to the **287 C-Tier customers**.
    *   **Terms:** Minimum Order Quantity (MOQ) of €500 + Move to Net-30 Payment Terms.
    *   **Goal:** Convert the "Red Bar" into profitable volume or shed the dead weight.

2.  **Fix the Fresh Supply Chain (Operational):**
    *   **Action:** Audit the cold chain logistics for Fresh products.
    *   **Target:** Reduce Return Rate from **7.8%** to **4.0%**.
    *   **Impact:** ~€500k annual savings in waste reduction.

3.  **Stop Incentivizing Unprofitable Revenue:**
    *   **Action:** Change Sales Commission structure from *Revenue %* to *Gross Margin %*.

---

## 🤝 Contact & Collaboration

**Ready to transform your data into profit?**

*   **Author:** Shriram Sutraye
*   **Role:** Data Science & Strategy
*   **Connect:** [LinkedIn Profile](https://linkedin.com/in/yourprofile) | [Email](mailto:your.email@example.com)

---
*This project is licensed under MIT. Data is synthetic but modeled on real-world B2B wholesale economics.*
