import pandas as pd
import numpy as np
import sys

print("=" * 100)
print("DATASET 11: CUSTOMER LIFETIME VALUE (CLV)")
print("Strategic customer segmentation for decision-making")
print("=" * 100)

# Load data
print("\n[STEP 1] Loading datasets...")
try:
    customers = pd.read_csv('data/processed/01_customer_master.csv')
    pnl_orders = pd.read_csv('data/generated/10_financial_p_l_orders.csv')
    print(f"✓ Loaded {len(customers)} customers")
    print(f"✓ Loaded {len(pnl_orders)} orders")
except FileNotFoundError as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

# Customer Lifetime Parameters
print("\n[STEP 2] Setting CLV parameters...")

# Expected customer lifetime by segment (industry standard - food wholesale)
customer_lifetime_years = {
    'SMB': 2.5,           # High churn, opportunistic
    'Mid-Market': 6.0,    # Moderate loyalty
    'Enterprise': 12.0    # Sticky, strategic relationships
}

# Acquisition cost per customer (one-time, industry average)
acquisition_cost = {
    'SMB': 300,           # Low-touch acquisition
    'Mid-Market': 2000,   # Moderate sales effort
    'Enterprise': 10000   # High-touch, executive engagement
}

# Discount rate for NPV calculation (optional - use 0% for simple version)
discount_rate = 0.0  # 0% = simple calculation, 5% = NPV-based

print(f"✓ Customer Lifetimes: SMB {customer_lifetime_years['SMB']}yr, Mid {customer_lifetime_years['Mid-Market']}yr, Ent {customer_lifetime_years['Enterprise']}yr")
print(f"✓ Acquisition Costs: SMB €{acquisition_cost['SMB']}, Mid €{acquisition_cost['Mid-Market']}, Ent €{acquisition_cost['Enterprise']}")

# Step 3: Calculate annual profit per customer
print("\n[STEP 3] Calculating annual profit per customer...")

annual_profit_by_customer = pnl_orders.groupby('CustomerID').agg({
    'Profit_EUR': 'sum',
    'TransactionAmount': 'count',  # number of orders
    'CustomerSegment': 'first'
}).rename(columns={'Profit_EUR': 'AnnualProfit_EUR', 'TransactionAmount': 'OrderCount'})

print(f"✓ Calculated profit for {len(annual_profit_by_customer)} customers")

# Step 4: Start with customers, add profit data
print("\n[STEP 4] Merging with P&L data...")

clv_data = customers[['CustomerID', 'CustomerName', 'CustomerSegment']].copy()
clv_data = clv_data.merge(annual_profit_by_customer[['AnnualProfit_EUR', 'OrderCount']], 
                          left_on='CustomerID', right_index=True, how='left')

# Fill missing values (customers with no orders)
clv_data['AnnualProfit_EUR'] = clv_data['AnnualProfit_EUR'].fillna(0)
clv_data['OrderCount'] = clv_data['OrderCount'].fillna(0).astype(int)

print(f"✓ Merged with {len(clv_data)} customers")

# Step 5: Calculate CLV metrics
print("\n[STEP 5] Calculating CLV metrics...")

clv_data['ExpectedLifetime_Years'] = clv_data['CustomerSegment'].map(customer_lifetime_years)
clv_data['AcquisitionCost_EUR'] = clv_data['CustomerSegment'].map(acquisition_cost)

# CLV = (Annual Profit × Expected Lifetime) - Acquisition Cost
clv_data['CLV_EUR'] = (clv_data['AnnualProfit_EUR'] * clv_data['ExpectedLifetime_Years']) - clv_data['AcquisitionCost_EUR']

# CLV with discount rate (NPV)
if discount_rate > 0:
    clv_data['CLV_NPV_EUR'] = 0
    for year in range(1, int(clv_data['ExpectedLifetime_Years'].max()) + 1):
        clv_data['CLV_NPV_EUR'] += clv_data['AnnualProfit_EUR'] / ((1 + discount_rate) ** year)
    clv_data['CLV_NPV_EUR'] -= clv_data['AcquisitionCost_EUR']
else:
    clv_data['CLV_NPV_EUR'] = clv_data['CLV_EUR']

# CLV as multiple of acquisition cost
clv_data['PaybackMultiple'] = clv_data['CLV_EUR'] / clv_data['AcquisitionCost_EUR'].replace(0, 1)

# Profitability margin
clv_data['CLVMargin_Pct'] = (clv_data['CLV_EUR'] / (clv_data['AnnualProfit_EUR'] * clv_data['ExpectedLifetime_Years']).replace(0, 1) * 100).round(2)

# Classify customers
def classify_customer(clv):
    if clv > 5000:
        return 'A-Customer'
    elif clv > 0:
        return 'B-Customer'
    else:
        return 'C-Customer'

clv_data['CLVSegment'] = clv_data['CLV_EUR'].apply(classify_customer)

# Action recommendation
def recommend_action(segment, clv):
    if segment == 'A-Customer':
        return 'INVEST & EXPAND'
    elif segment == 'B-Customer':
        return 'MAINTAIN & MONITOR'
    elif clv < -1000:
        return 'EXIT IMMEDIATELY'
    else:
        return 'RENEGOTIATE TERMS'

clv_data['RecommendedAction'] = clv_data.apply(lambda row: recommend_action(row['CLVSegment'], row['CLV_EUR']), axis=1)

print(f"✓ Calculated CLV for all customers")

# Step 6: Create summary statistics
print("\n[STEP 6] Generating summaries...")

# Summary by segment
segment_summary = clv_data.groupby('CustomerSegment').agg({
    'CustomerID': 'count',
    'AnnualProfit_EUR': ['sum', 'mean'],
    'OrderCount': 'mean',
    'CLV_EUR': ['sum', 'mean', 'min', 'max'],
    'CLVSegment': lambda x: (x == 'A-Customer').sum()
}).round(2)

segment_summary.columns = ['CustomerCount', 'AnnualProfit_Total', 'AnnualProfit_Avg', 'OrderCount_Avg',
                          'CLV_Total', 'CLV_Avg', 'CLV_Min', 'CLV_Max', 'ACustomerCount']

# Summary by CLV segment
clv_segment_summary = clv_data.groupby('CLVSegment').agg({
    'CustomerID': 'count',
    'CLV_EUR': ['sum', 'mean'],
    'AnnualProfit_EUR': 'sum',
    'OrderCount': 'mean'
}).round(2)

clv_segment_summary.columns = ['CustomerCount', 'CLV_Total', 'CLV_Avg', 'AnnualProfit_Total', 'OrderCount_Avg']

# Action summary
action_summary = clv_data.groupby('RecommendedAction').agg({
    'CustomerID': 'count',
    'CLV_EUR': 'sum',
    'AnnualProfit_EUR': 'sum'
}).round(2)
action_summary.columns = ['CustomerCount', 'CLV_Total', 'AnnualProfit_Total']

print(f"✓ Generated segment, CLV segment, and action summaries")

# Step 7: Save files
print("\n[STEP 7] Saving datasets...")

clv_data.to_csv('data/generated/11_customer_lifetime_value.csv', index=False)
segment_summary.to_csv('data/generated/11_clv_by_segment_summary.csv')
clv_segment_summary.to_csv('data/generated/11_clv_segment_summary.csv')
action_summary.to_csv('data/generated/11_clv_action_summary.csv')

print(f"✓ Saved: 11_customer_lifetime_value.csv ({len(clv_data)} rows)")
print(f"✓ Saved: 11_clv_by_segment_summary.csv")
print(f"✓ Saved: 11_clv_segment_summary.csv")
print(f"✓ Saved: 11_clv_action_summary.csv")

# Print summaries
print("\n" + "=" * 100)
print("DATASET 11 GENERATION SUMMARY")
print("=" * 100)

print(f"\n[BY ORIGINAL SEGMENT]:")
print(segment_summary)

print(f"\n[BY CLV CLASSIFICATION]:")
print(clv_segment_summary)

print(f"\n[BY RECOMMENDED ACTION]:")
print(action_summary)

print(f"\n[KEY INSIGHTS]:")
a_customers = len(clv_data[clv_data['CLVSegment'] == 'A-Customer'])
b_customers = len(clv_data[clv_data['CLVSegment'] == 'B-Customer'])
c_customers = len(clv_data[clv_data['CLVSegment'] == 'C-Customer'])
total_clv = clv_data['CLV_EUR'].sum()

a_clv = clv_data[clv_data['CLVSegment']=='A-Customer']['CLV_EUR'].sum()
b_clv = clv_data[clv_data['CLVSegment']=='B-Customer']['CLV_EUR'].sum()
c_clv = clv_data[clv_data['CLVSegment']=='C-Customer']['CLV_EUR'].sum()

print(f"  A-Customers: {a_customers} ({a_customers/len(clv_data)*100:.1f}%) - €{a_clv:,.0f} total CLV")
print(f"  B-Customers: {b_customers} ({b_customers/len(clv_data)*100:.1f}%) - €{b_clv:,.0f} total CLV")
print(f"  C-Customers: {c_customers} ({c_customers/len(clv_data)*100:.1f}%) - €{c_clv:,.0f} total CLV (NEGATIVE)")
print(f"  Total Lifetime Value: €{total_clv:,.0f}")

exit_candidates = len(clv_data[clv_data['CLV_EUR'] < -1000])
print(f"\n  Candidates for EXIT (CLV < -€1,000): {exit_candidates} customers")
print(f"  Candidates for RENEGOTIATION (CLV -€1k to 0): {c_customers - exit_candidates} customers")
print(f"  Strong performers (CLV > €5k): {a_customers} customers worth investing in")

print("\n" + "=" * 100)
print("✓ DATASET 11 GENERATION COMPLETE")
print("=" * 100)

