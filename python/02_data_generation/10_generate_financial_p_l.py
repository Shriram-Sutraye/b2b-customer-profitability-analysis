import pandas as pd
import numpy as np
import sys

print("=" * 100)
print("DATASET 10: FINANCIAL P&L - COMPLETE COST-TO-SERVE ANALYSIS")
print("All inclusive: 14,488 orders + segment/product rollups + matrix")
print("=" * 100)

# Load all datasets
print("\n[STEP 1] Loading all datasets...")
try:
    transactions = pd.read_csv('data/generated/02_transactions_generated.csv')
    warehouse = pd.read_csv('data/generated/04_warehouse_costs_generated.csv')
    shipping = pd.read_csv('data/generated/05_shipping_costs_generated.csv')
    returns = pd.read_csv('data/generated/06_returns_handling_generated.csv')
    interest = pd.read_csv('data/generated/07_payment_terms_interest_generated.csv')
    overhead = pd.read_csv('data/generated/09_admin_overhead_generated.csv')
    customers = pd.read_csv('data/processed/01_customer_master.csv')
    print(f"✓ Loaded all cost datasets")
except FileNotFoundError as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

# Merge all data
print("\n[STEP 2] Merging all datasets...")
pnl = transactions.copy()
pnl = pnl.merge(warehouse[['TransactionID', 'TotalWarehouseOperationsCost_EUR']], on='TransactionID', how='left')
pnl = pnl.merge(shipping[['TransactionID', 'TotalShippingCost_EUR']], on='TransactionID', how='left')
pnl = pnl.merge(returns[['TransactionID', 'TotalReturnExpense_EUR']], on='TransactionID', how='left')
pnl = pnl.merge(interest[['TransactionID', 'DSO_InterestCost_EUR', 'PaymentTerms']], on='TransactionID', how='left')
pnl = pnl.merge(overhead[['TransactionID', 'TotalAllocatedOverhead_EUR', 'CustomerSegment']], on='TransactionID', how='left')

print(f"✓ Merged all datasets into {len(pnl)} rows")

# Calculate COGS (from transactions - it's embedded)
print("\n[STEP 3] Calculating P&L components...")

# Standard COGS (60% of revenue from Datasets 1-3)
pnl['COGS_EUR'] = pnl['TransactionAmount'] * 0.60

# Warehouse (from Dataset 4)
pnl['WarehouseCost_EUR'] = pnl['TotalWarehouseOperationsCost_EUR'].fillna(0)

# Shipping (from Dataset 5)
pnl['ShippingCost_EUR'] = pnl['TotalShippingCost_EUR'].fillna(0)

# Returns (from Dataset 6)
pnl['ReturnsCost_EUR'] = pnl['TotalReturnExpense_EUR'].fillna(0)

# Interest (from Dataset 7)
pnl['InterestCost_EUR'] = pnl['DSO_InterestCost_EUR'].fillna(0)

# Overhead (from Dataset 9)
pnl['OverheadCost_EUR'] = pnl['TotalAllocatedOverhead_EUR'].fillna(0)

# Total Cost-to-Serve
pnl['TotalCost_EUR'] = (pnl['COGS_EUR'] + pnl['WarehouseCost_EUR'] + pnl['ShippingCost_EUR'] + 
                        pnl['ReturnsCost_EUR'] + pnl['InterestCost_EUR'] + pnl['OverheadCost_EUR'])

# Profit
pnl['Profit_EUR'] = pnl['TransactionAmount'] - pnl['TotalCost_EUR']

# Profit Margin %
pnl['ProfitMargin_Pct'] = (pnl['Profit_EUR'] / pnl['TransactionAmount'] * 100).round(2)

# Cost as % of Revenue
pnl['CostToRevenue_Pct'] = (pnl['TotalCost_EUR'] / pnl['TransactionAmount'] * 100).round(2)

# Profitability Category
def categorize_profit(profit, margin):
    if profit > 50:
        return 'Highly Profitable'
    elif profit > 0:
        return 'Profitable'
    elif profit > -25:
        return 'Breakeven'
    else:
        return 'Loss'

pnl['ProfitabilityCategory'] = pnl.apply(lambda row: categorize_profit(row['Profit_EUR'], row['ProfitMargin_Pct']), axis=1)

# Action Flags
pnl['ShouldRaisePrice'] = pnl['Profit_EUR'] < 0
pnl['ShouldReduceCost'] = pnl['CostToRevenue_Pct'] > 95
pnl['ShouldReviewCustomer'] = (pnl['Profit_EUR'] < 0) | (pnl['CostToRevenue_Pct'] > 95)

print(f"✓ Calculated all P&L metrics")

# Select final columns for P&L
pnl_columns = [
    'TransactionID', 'CustomerID', 'CustomerSegment', 'ProductCategory', 
    'OrderMonth', 'PaymentTerms', 'IsStandardOrder', 'IsUrgent',
    'TransactionAmount', 'COGS_EUR', 'WarehouseCost_EUR', 'ShippingCost_EUR',
    'ReturnsCost_EUR', 'InterestCost_EUR', 'OverheadCost_EUR', 'TotalCost_EUR',
    'Profit_EUR', 'ProfitMargin_Pct', 'CostToRevenue_Pct',
    'ProfitabilityCategory', 'ShouldRaisePrice', 'ShouldReduceCost', 'ShouldReviewCustomer'
]

pnl_final = pnl[pnl_columns].copy()

# Round all monetary columns
for col in ['TransactionAmount', 'COGS_EUR', 'WarehouseCost_EUR', 'ShippingCost_EUR', 
            'ReturnsCost_EUR', 'InterestCost_EUR', 'OverheadCost_EUR', 'TotalCost_EUR', 'Profit_EUR']:
    pnl_final[col] = pnl_final[col].round(2)

print(f"\n[STEP 4] Creating aggregations...")

# Aggregation 1: By Segment
segment_summary = pnl_final.groupby('CustomerSegment').agg({
    'TransactionAmount': ['sum', 'mean', 'count'],
    'COGS_EUR': 'sum',
    'WarehouseCost_EUR': 'sum',
    'ShippingCost_EUR': 'sum',
    'ReturnsCost_EUR': 'sum',
    'InterestCost_EUR': 'sum',
    'OverheadCost_EUR': 'sum',
    'TotalCost_EUR': 'sum',
    'Profit_EUR': ['sum', 'mean'],
    'ProfitMargin_Pct': 'mean'
}).round(2)
segment_summary.columns = ['Revenue_Total', 'Revenue_Avg', 'Order_Count', 'COGS_Total', 'Warehouse_Total',
                          'Shipping_Total', 'Returns_Total', 'Interest_Total', 'Overhead_Total', 'TotalCost_Total',
                          'Profit_Total', 'Profit_Avg', 'ProfitMargin_Avg_Pct']

# Aggregation 2: By Product
product_summary = pnl_final.groupby('ProductCategory').agg({
    'TransactionAmount': ['sum', 'mean', 'count'],
    'COGS_EUR': 'sum',
    'WarehouseCost_EUR': 'sum',
    'ShippingCost_EUR': 'sum',
    'ReturnsCost_EUR': 'sum',
    'InterestCost_EUR': 'sum',
    'OverheadCost_EUR': 'sum',
    'TotalCost_EUR': 'sum',
    'Profit_EUR': ['sum', 'mean'],
    'ProfitMargin_Pct': 'mean'
}).round(2)
product_summary.columns = ['Revenue_Total', 'Revenue_Avg', 'Order_Count', 'COGS_Total', 'Warehouse_Total',
                          'Shipping_Total', 'Returns_Total', 'Interest_Total', 'Overhead_Total', 'TotalCost_Total',
                          'Profit_Total', 'Profit_Avg', 'ProfitMargin_Avg_Pct']

# Aggregation 3: By Segment + Product (Matrix)
segment_product_matrix = pnl_final.groupby(['CustomerSegment', 'ProductCategory']).agg({
    'Profit_EUR': ['sum', 'mean', 'count'],
    'ProfitMargin_Pct': 'mean',
    'TransactionAmount': 'sum'
}).round(2)
segment_product_matrix.columns = ['Profit_Total', 'Profit_Avg', 'Order_Count', 'ProfitMargin_Avg_Pct', 'Revenue_Total']

# Aggregation 4: Overall P&L
overall_summary = pd.DataFrame({
    'Metric': ['Total Revenue', 'Total COGS', 'Total Warehouse', 'Total Shipping', 'Total Returns',
               'Total Interest', 'Total Overhead', 'Total Cost-to-Serve', 'Total Profit', 'Overall Margin %'],
    'Amount': [
        pnl_final['TransactionAmount'].sum(),
        pnl_final['COGS_EUR'].sum(),
        pnl_final['WarehouseCost_EUR'].sum(),
        pnl_final['ShippingCost_EUR'].sum(),
        pnl_final['ReturnsCost_EUR'].sum(),
        pnl_final['InterestCost_EUR'].sum(),
        pnl_final['OverheadCost_EUR'].sum(),
        pnl_final['TotalCost_EUR'].sum(),
        pnl_final['Profit_EUR'].sum(),
        (pnl_final['Profit_EUR'].sum() / pnl_final['TransactionAmount'].sum() * 100)
    ]
}).round(2)

print(f"✓ Created segment, product, and matrix summaries")

# Save all files
print(f"\n[STEP 5] Saving all P&L files...")

pnl_final.to_csv('data/generated/10_financial_p_l_orders.csv', index=False)
segment_summary.to_csv('data/generated/10_p_l_by_segment.csv')
product_summary.to_csv('data/generated/10_p_l_by_product.csv')
segment_product_matrix.to_csv('data/generated/10_p_l_segment_product_matrix.csv')
overall_summary.to_csv('data/generated/10_p_l_overall_summary.csv', index=False)

print(f"✓ Saved: 10_financial_p_l_orders.csv ({len(pnl_final)} rows)")
print(f"✓ Saved: 10_p_l_by_segment.csv ({len(segment_summary)} rows)")
print(f"✓ Saved: 10_p_l_by_product.csv ({len(product_summary)} rows)")
print(f"✓ Saved: 10_p_l_segment_product_matrix.csv ({len(segment_product_matrix)} rows)")
print(f"✓ Saved: 10_p_l_overall_summary.csv ({len(overall_summary)} rows)")

# Print summaries
print("\n" + "=" * 100)
print("DATASET 10 GENERATION SUMMARY")
print("=" * 100)

print("\n[OVERALL P&L]:")
for _, row in overall_summary.iterrows():
    print(f"  {row['Metric']}: €{row['Amount']:,.2f}")

print("\n[BY CUSTOMER SEGMENT]:")
for segment in segment_summary.index:
    profit = segment_summary.loc[segment, 'Profit_Total']
    margin = segment_summary.loc[segment, 'ProfitMargin_Avg_Pct']
    orders = segment_summary.loc[segment, 'Order_Count']
    print(f"  {segment}: €{profit:,.2f} total ({margin:.2f}% margin, {int(orders)} orders)")

print("\n[BY PRODUCT CATEGORY]:")
for product in product_summary.index:
    profit = product_summary.loc[product, 'Profit_Total']
    margin = product_summary.loc[product, 'ProfitMargin_Avg_Pct']
    orders = product_summary.loc[product, 'Order_Count']
    print(f"  {product}: €{profit:,.2f} total ({margin:.2f}% margin, {int(orders)} orders)")

print("\n[PROFITABILITY CATEGORIES]:")
category_counts = pnl_final['ProfitabilityCategory'].value_counts()
for category, count in category_counts.items():
    pct = count / len(pnl_final) * 100
    print(f"  {category}: {count} orders ({pct:.1f}%)")

print("\n[ACTION FLAGS]:")
price_flag = pnl_final['ShouldRaisePrice'].sum()
cost_flag = pnl_final['ShouldReduceCost'].sum()
review_flag = pnl_final['ShouldReviewCustomer'].sum()
print(f"  Orders needing price increase: {price_flag} ({price_flag/len(pnl_final)*100:.1f}%)")
print(f"  Orders needing cost reduction: {cost_flag} ({cost_flag/len(pnl_final)*100:.1f}%)")
print(f"  Orders needing review: {review_flag} ({review_flag/len(pnl_final)*100:.1f}%)")

print("\n" + "=" * 100)
print("✓ DATASET 10 GENERATION COMPLETE")
print("=" * 100)

