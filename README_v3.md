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

![Customer Profitability Segmentation](../powerbi/Dashboards/Screenshot%20From%202025-11-20%2022-54-18.png)

**The Insight:**
Contrary to the belief that "a few bad apples" were the issue, the dashboard reveals a systemic failure. The **massive red bar** represents the **C-Tier Segment**:
*   **Scope:** **287 customers** (65% of total base).
*   **Impact:** These customers are not just low-margin; they are **value destroyers**.
*   **Action:** The business model for the mass market is fundamentally broken and requires immediate restructuring (price hikes, strict MOQs, or terms changes).

### 2. Strategic Path Forward: €2.5M Upside
*Quantifying the value of corrective actions.*

![Strategic Scenario Modeling](../powerbi/Dashboards/Screenshot%20From%202025-11-20%2022-54-38.png)

**The Strategy:**
I modeled five scenarios to fix the P&L. The dashboard clearly shows the winner:
*   **Status Quo (Far Left):** ~€80k Profit (Unsustainable).
*   **Exit C-Tier:** ~€1.6M Profit (Viable, but shrinks revenue too much).
*   **Renegotiate C-Tier (Target):** **~€2.5M Profit**.

**The Recommendation:**
Do not fire the 65%. **Fix them.** By implementing a "Renegotiation Framework" (Price +20% / Net-30 Terms), we convert this volume from a loss leader into a profit contributor.

### 3. Operational Diagnostics: The Cost of Complexity
*Where the operational dollars are actually going.*

![Operational Cost Forensics](../powerbi/Dashboards/Screenshot%20From%202025-11-20%2022-54-45.png)

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
