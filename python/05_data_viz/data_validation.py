# FILE: /python/05_data_viz/data_validation.py
# Data Validation & Metrics Calculation (No Visualizations)
# Outputs: Console print + CSV files for validation

import pandas as pd
import numpy as np

# File paths (adjust if needed)
clv_path = '../../data/generated/11_customer_lifetime_value.csv'
orders_path = '../../data/generated/10_financial_p_l_orders.csv'
cust_path = '../../data/processed/01_customer_master.csv'

# Load data
print("="*80)
print("LOADING DATA...")
print("="*80)
clv = pd.read_csv(clv_path)
orders = pd.read_csv(orders_path)
cust = pd.read_csv(cust_path)

print(f"✅ CLV Table: {clv.shape[0]} rows, {clv.shape[1]} columns")
print(f"✅ Orders Table: {orders.shape[0]} rows, {orders.shape[1]} columns")
print(f"✅ Customer Master: {cust.shape[0]} rows, {cust.shape[1]} columns")

# ============================================================================
# SECTION 1: EXECUTIVE KPIs (CLV TABLE)
# ============================================================================
print("\n" + "="*80)
print("SECTION 1: EXECUTIVE KPIs (FROM CLV TABLE)")
print("="*80)

kpis_clv = {
    "Total CLV (€)": clv['CLV_EUR'].sum(),
    "Total Annual Profit (€)": clv['AnnualProfit_EUR'].sum(),
    "Average CLV per Customer (€)": clv['CLV_EUR'].mean(),
    "Average Annual Profit per Customer (€)": clv['AnnualProfit_EUR'].mean(),
    "Customer Count": clv['CustomerID'].nunique(),
    "Average CLV Margin (%)": clv['CLVMargin_Pct'].mean(),
    "Median CLV (€)": clv['CLV_EUR'].median(),
    "Total Acquisition Cost (€)": clv['AcquisitionCost_EUR'].sum(),
    "Average Payback Multiple": clv['PaybackMultiple'].mean(),
}

for k, v in kpis_clv.items():
    print(f"{k:45s}: {v:>15,.2f}")

# ============================================================================
# SECTION 2: SEGMENTATION BREAKDOWN
# ============================================================================
print("\n" + "="*80)
print("SECTION 2: SEGMENTATION BREAKDOWN")
print("="*80)

# CLV Segment counts
print("\n--- Customer Count by CLV Segment ---")
clv_seg_counts = clv['CLVSegment'].value_counts().sort_index()
print(clv_seg_counts)
print(f"Total: {clv_seg_counts.sum()}")

# CLV Segment totals
print("\n--- Total CLV by CLV Segment ---")
clv_seg_totals = clv.groupby('CLVSegment')['CLV_EUR'].sum().sort_index()
print(clv_seg_totals)

print("\n--- Total Profit by CLV Segment ---")
profit_seg_totals = clv.groupby('CLVSegment')['AnnualProfit_EUR'].sum().sort_index()
print(profit_seg_totals)

# Customer Segment (from CLV table if exists)
if 'CustomerSegment' in clv.columns:
    print("\n--- Customer Count by Customer Segment ---")
    cust_seg_counts = clv['CustomerSegment'].value_counts().sort_index()
    print(cust_seg_counts)

# ============================================================================
# SECTION 3: ORDERS TABLE METRICS
# ============================================================================
print("\n" + "="*80)
print("SECTION 3: ORDERS TABLE METRICS")
print("="*80)

kpis_orders = {
    "Total Transaction Amount (Revenue) (€)": orders['TransactionAmount'].sum(),
    "Total COGS (€)": orders['COGS_EUR'].sum(),
    "Total Profit (€)": orders['Profit_EUR'].sum(),
    "Average Profit Margin (%)": orders['ProfitMargin_Pct'].mean(),
    "Order Count": orders['TransactionID'].nunique(),
    "Average Transaction Amount (€)": orders['TransactionAmount'].mean(),
    "Total Warehouse Cost (€)": orders['WarehouseCost_EUR'].sum(),
    "Total Shipping Cost (€)": orders['ShippingCost_EUR'].sum(),
    "Total Returns Cost (€)": orders['ReturnsCost_EUR'].sum(),
    "Total Interest Cost (€)": orders['InterestCost_EUR'].sum(),
    "Total Overhead Cost (€)": orders['OverheadCost_EUR'].sum(),
}

for k, v in kpis_orders.items():
    print(f"{k:45s}: {v:>15,.2f}")

# Calculate Gross Margin & Net Margin
gross_profit = orders['TransactionAmount'].sum() - orders['COGS_EUR'].sum()
gross_margin_pct = (gross_profit / orders['TransactionAmount'].sum()) * 100
net_margin_pct = (orders['Profit_EUR'].sum() / orders['TransactionAmount'].sum()) * 100

print(f"\n{'Gross Profit (€)':45s}: {gross_profit:>15,.2f}")
print(f"{'Gross Margin (%)':45s}: {gross_margin_pct:>15,.2f}")
print(f"{'Net Margin (%)':45s}: {net_margin_pct:>15,.2f}")

# ============================================================================
# SECTION 4: MONTHLY TRENDS (if OrderMonth exists)
# ============================================================================
if 'OrderMonth' in orders.columns:
    print("\n" + "="*80)
    print("SECTION 4: MONTHLY TRENDS")
    print("="*80)
    
    orders['OrderMonth'] = pd.to_datetime(orders['OrderMonth'], errors='coerce')
    monthly = orders.groupby(orders['OrderMonth'].dt.to_period('M')).agg({
        'TransactionAmount': 'sum',
        'Profit_EUR': 'sum',
        'TransactionID': 'count'
    }).rename(columns={'TransactionID': 'OrderCount'})
    
    print(monthly)
    monthly.to_csv('monthly_trends.csv')
    print("\n✅ Saved to: monthly_trends.csv")

# ============================================================================
# SECTION 5: TOP/BOTTOM CUSTOMERS
# ============================================================================
print("\n" + "="*80)
print("SECTION 5: TOP/BOTTOM CUSTOMERS")
print("="*80)

print("\n--- Top 10 Customers by CLV ---")
top10_clv = clv.nlargest(10, 'CLV_EUR')[['CustomerID', 'CustomerName', 'CLV_EUR', 'AnnualProfit_EUR', 'CLVSegment']]
print(top10_clv.to_string(index=False))

print("\n--- Bottom 10 Customers by CLV ---")
bottom10_clv = clv.nsmallest(10, 'CLV_EUR')[['CustomerID', 'CustomerName', 'CLV_EUR', 'AnnualProfit_EUR', 'CLVSegment']]
print(bottom10_clv.to_string(index=False))

print("\n--- Top 10 Customers by Annual Profit ---")
top10_profit = clv.nlargest(10, 'AnnualProfit_EUR')[['CustomerID', 'CustomerName', 'CLV_EUR', 'AnnualProfit_EUR', 'CLVSegment']]
print(top10_profit.to_string(index=False))

print("\n--- Bottom 10 Customers by Annual Profit ---")
bottom10_profit = clv.nsmallest(10, 'AnnualProfit_EUR')[['CustomerID', 'CustomerName', 'CLV_EUR', 'AnnualProfit_EUR', 'CLVSegment']]
print(bottom10_profit.to_string(index=False))

# ============================================================================
# SECTION 6: DATA QUALITY CHECKS
# ============================================================================
print("\n" + "="*80)
print("SECTION 6: DATA QUALITY CHECKS")
print("="*80)

print("\n--- NULL COUNTS (CLV Table) ---")
print(clv.isnull().sum())

print("\n--- NULL COUNTS (Orders Table) ---")
print(orders.isnull().sum())

print("\n--- NEGATIVE VALUES CHECK (CLV Table) ---")
print(f"Negative CLV values: {(clv['CLV_EUR'] < 0).sum()}")
print(f"Negative Profit values: {(clv['AnnualProfit_EUR'] < 0).sum()}")

print("\n--- NEGATIVE VALUES CHECK (Orders Table) ---")
print(f"Negative Profit values: {(orders['Profit_EUR'] < 0).sum()}")
print(f"Negative Transaction Amount: {(orders['TransactionAmount'] < 0).sum()}")

# ============================================================================
# SECTION 7: PRODUCT CATEGORY ANALYSIS (if exists)
# ============================================================================
if 'ProductCategory' in orders.columns:
    print("\n" + "="*80)
    print("SECTION 7: PRODUCT CATEGORY ANALYSIS")
    print("="*80)
    
    cat_agg = orders.groupby('ProductCategory').agg({
        'TransactionAmount': 'sum',
        'Profit_EUR': 'sum',
        'TransactionID': 'count'
    }).rename(columns={'TransactionID': 'OrderCount'}).sort_values('Profit_EUR', ascending=False)
    
    print(cat_agg)

# ============================================================================
# SECTION 8: PROFITABILITY CATEGORY BREAKDOWN (if exists)
# ============================================================================
if 'ProfitabilityCategory' in orders.columns:
    print("\n" + "="*80)
    print("SECTION 8: PROFITABILITY CATEGORY BREAKDOWN")
    print("="*80)
    
    prof_cat = orders['ProfitabilityCategory'].value_counts().sort_index()
    print(prof_cat)

# ============================================================================
# SECTION 9: RECOMMENDED ACTIONS (if exists)
# ============================================================================
if 'RecommendedAction' in clv.columns:
    print("\n" + "="*80)
    print("SECTION 9: RECOMMENDED ACTIONS")
    print("="*80)
    
    actions = clv['RecommendedAction'].value_counts().sort_index()
    print(actions)

# ============================================================================
# SECTION 10: EXPORT SUMMARY TO CSV
# ============================================================================
print("\n" + "="*80)
print("SECTION 10: EXPORTING SUMMARY DATA")
print("="*80)

# Export KPI summary
kpi_summary = pd.DataFrame([
    {"Metric": "Total CLV (€)", "Value": clv['CLV_EUR'].sum()},
    {"Metric": "Total Annual Profit (€)", "Value": clv['AnnualProfit_EUR'].sum()},
    {"Metric": "Customer Count", "Value": clv['CustomerID'].nunique()},
    {"Metric": "Avg CLV Margin (%)", "Value": clv['CLVMargin_Pct'].mean()},
    {"Metric": "Total Orders Revenue (€)", "Value": orders['TransactionAmount'].sum()},
    {"Metric": "Total Orders Profit (€)", "Value": orders['Profit_EUR'].sum()},
    {"Metric": "Gross Margin (%)", "Value": gross_margin_pct},
    {"Metric": "Net Margin (%)", "Value": net_margin_pct},
    {"Metric": "Order Count", "Value": orders['TransactionID'].nunique()},
])
kpi_summary.to_csv('kpi_summary.csv', index=False)
print("✅ Saved to: kpi_summary.csv")

# Export segment summary
seg_summary = clv.groupby('CLVSegment').agg({
    'CustomerID': 'count',
    'CLV_EUR': 'sum',
    'AnnualProfit_EUR': 'sum'
}).rename(columns={'CustomerID': 'CustomerCount'})
seg_summary.to_csv('segment_summary.csv')
print("✅ Saved to: segment_summary.csv")

print("\n" + "="*80)
print("✅ DATA VALIDATION COMPLETE!")
print("="*80)
print("Use these numbers as your SOURCE OF TRUTH for Power BI comparison.")
print("If Power BI numbers differ, check relationships/filters/DAX formulas.")

# EOF
