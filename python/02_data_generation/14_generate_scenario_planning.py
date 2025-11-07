import pandas as pd
import numpy as np
import sys

print("=" * 100)
print("DATASET 14: SCENARIO PLANNING - STRATEGIC DECISION MODELING")
print("What-if analysis for customer segmentation decisions")
print("=" * 100)

# Load data
print("\n[STEP 1] Loading datasets...")
try:
    pnl_orders = pd.read_csv('data/generated/10_financial_p_l_orders.csv')
    clv_customers = pd.read_csv('data/generated/11_customer_lifetime_value.csv')
    print(f"✓ Loaded {len(pnl_orders)} orders")
    print(f"✓ Loaded {len(clv_customers)} customers")
except FileNotFoundError as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

# Get baseline metrics
print("\n[STEP 2] Calculating baseline (Status Quo)...")

baseline_revenue = pnl_orders['TransactionAmount'].sum()
baseline_cogs = pnl_orders['COGS_EUR'].sum()
baseline_warehouse = pnl_orders['WarehouseCost_EUR'].sum()
baseline_shipping = pnl_orders['ShippingCost_EUR'].sum()
baseline_returns = pnl_orders['ReturnsCost_EUR'].sum()
baseline_interest = pnl_orders['InterestCost_EUR'].sum()
baseline_overhead = pnl_orders['OverheadCost_EUR'].sum()
baseline_total_cost = baseline_cogs + baseline_warehouse + baseline_shipping + baseline_returns + baseline_interest + baseline_overhead
baseline_profit = baseline_revenue - baseline_total_cost
baseline_margin = (baseline_profit / baseline_revenue * 100) if baseline_revenue > 0 else 0

print(f"✓ Revenue: €{baseline_revenue:,.2f}")
print(f"✓ Total Costs: €{baseline_total_cost:,.2f}")
print(f"✓ Profit: €{baseline_profit:,.2f}")
print(f"✓ Margin: {baseline_margin:.2f}%")

# Get customer tiers from CLV (extract as sets of IDs)
print("\n[STEP 3] Extracting customer tiers from CLV...")

a_customers = set(clv_customers[clv_customers['CLVSegment'] == 'A-Customer']['CustomerID'].unique())
b_customers = set(clv_customers[clv_customers['CLVSegment'] == 'B-Customer']['CustomerID'].unique())
c_customers = set(clv_customers[clv_customers['CLVSegment'] == 'C-Customer']['CustomerID'].unique())

smb_customers = set(clv_customers[clv_customers['CustomerSegment'] == 'SMB']['CustomerID'].unique())
mid_customers = set(clv_customers[clv_customers['CustomerSegment'] == 'Mid-Market']['CustomerID'].unique())
ent_customers = set(clv_customers[clv_customers['CustomerSegment'] == 'Enterprise']['CustomerID'].unique())

print(f"✓ A-Customers: {len(a_customers)}")
print(f"✓ B-Customers: {len(b_customers)}")
print(f"✓ C-Customers: {len(c_customers)}")
print(f"✓ SMB: {len(smb_customers)}, Mid: {len(mid_customers)}, Enterprise: {len(ent_customers)}")

# Build scenarios
print("\n[STEP 4] Building 5 scenarios...")

scenarios = {}

# Scenario 1: Status Quo (all customers)
print("\n[SCENARIO 1] Status Quo - Keep all 440 customers")
s1_customers = set(pnl_orders['CustomerID'].unique())
s1_revenue = pnl_orders['TransactionAmount'].sum()
s1_cogs = pnl_orders['COGS_EUR'].sum()
s1_warehouse = pnl_orders['WarehouseCost_EUR'].sum()
s1_shipping = pnl_orders['ShippingCost_EUR'].sum()
s1_returns = pnl_orders['ReturnsCost_EUR'].sum()
s1_interest = pnl_orders['InterestCost_EUR'].sum()
s1_overhead = pnl_orders['OverheadCost_EUR'].sum()
s1_total_cost = s1_cogs + s1_warehouse + s1_shipping + s1_returns + s1_interest + s1_overhead
s1_profit = s1_revenue - s1_total_cost
s1_margin = (s1_profit / s1_revenue * 100) if s1_revenue > 0 else 0

scenarios['Status Quo'] = {
    'customers_kept': len(s1_customers),
    'a_kept': len(s1_customers & a_customers),
    'b_kept': len(s1_customers & b_customers),
    'c_kept': len(s1_customers & c_customers),
    'revenue': s1_revenue,
    'cogs': s1_cogs,
    'warehouse': s1_warehouse,
    'shipping': s1_shipping,
    'returns': s1_returns,
    'interest': s1_interest,
    'overhead': s1_overhead,
    'total_cost': s1_total_cost,
    'profit': s1_profit,
    'margin': s1_margin,
    'risk': 'VERY HIGH',
    'probability': 0,
    'timeline': 'Current',
    'recommendation': 'UNSUSTAINABLE'
}
print(f"  ✓ Customers: {len(s1_customers)}, Revenue: €{s1_revenue:,.0f}, Profit: €{s1_profit:,.0f}, Margin: {s1_margin:.2f}%")

# Scenario 2: Exit C-Customers (keep A+B only)
print("\n[SCENARIO 2] Exit C-Customers - Keep only A+B (153 customers)")
s2_customers = a_customers | b_customers
s2_orders = pnl_orders[pnl_orders['CustomerID'].isin(s2_customers)]
s2_revenue = s2_orders['TransactionAmount'].sum()
s2_cogs = s2_orders['COGS_EUR'].sum()
s2_warehouse = s2_orders['WarehouseCost_EUR'].sum()
s2_shipping = s2_orders['ShippingCost_EUR'].sum()
s2_returns = s2_orders['ReturnsCost_EUR'].sum()
s2_interest = s2_orders['InterestCost_EUR'].sum()
s2_overhead = s2_orders['OverheadCost_EUR'].sum()
s2_overhead_adjusted = s2_overhead * 0.7  # Reduce overhead 30%
s2_total_cost = s2_cogs + s2_warehouse + s2_shipping + s2_returns + s2_interest + s2_overhead_adjusted
s2_profit = s2_revenue - s2_total_cost
s2_margin = (s2_profit / s2_revenue * 100) if s2_revenue > 0 else 0

scenarios['Exit C-Customers'] = {
    'customers_kept': len(s2_customers),
    'a_kept': len(s2_customers & a_customers),
    'b_kept': len(s2_customers & b_customers),
    'c_kept': 0,
    'revenue': s2_revenue,
    'cogs': s2_cogs,
    'warehouse': s2_warehouse,
    'shipping': s2_shipping,
    'returns': s2_returns,
    'interest': s2_interest,
    'overhead': s2_overhead_adjusted,
    'total_cost': s2_total_cost,
    'profit': s2_profit,
    'margin': s2_margin,
    'risk': 'MEDIUM',
    'probability': 85,
    'timeline': '3-6 months',
    'recommendation': 'OPTIMAL'
}
print(f"  ✓ Customers: {len(s2_customers)}, Revenue: €{s2_revenue:,.0f}, Profit: €{s2_profit:,.0f}, Margin: {s2_margin:.2f}%")

# Scenario 3: Renegotiate C-Customers (+20% price, -25% volume)
print("\n[SCENARIO 3] Renegotiate C-Customers - +20% price, -25% volume loss")
# Filter by customer sets separately
s3_orders_ab = pnl_orders[pnl_orders['CustomerID'].isin(a_customers | b_customers)]
s3_orders_c_all = pnl_orders[pnl_orders['CustomerID'].isin(c_customers)]
# Sample 75% of C-customer orders
np.random.seed(42)
s3_orders_c = s3_orders_c_all.sample(frac=0.75)
# Combine
s3_orders = pd.concat([s3_orders_ab, s3_orders_c], ignore_index=True)
# Apply 20% price increase
s3_revenue = s3_orders['TransactionAmount'].sum() * 1.20
s3_cogs = s3_orders['COGS_EUR'].sum()
s3_warehouse = s3_orders['WarehouseCost_EUR'].sum()
s3_shipping = s3_orders['ShippingCost_EUR'].sum()
s3_returns = s3_orders['ReturnsCost_EUR'].sum()
s3_interest = s3_orders['InterestCost_EUR'].sum()
s3_overhead = s3_orders['OverheadCost_EUR'].sum() * 0.85  # Reduced overhead
s3_total_cost = s3_cogs + s3_warehouse + s3_shipping + s3_returns + s3_interest + s3_overhead
s3_profit = s3_revenue - s3_total_cost
s3_margin = (s3_profit / s3_revenue * 100) if s3_revenue > 0 else 0

s3_kept_customers = set(s3_orders['CustomerID'].unique())
scenarios['Renegotiate C'] = {
    'customers_kept': len(s3_kept_customers),
    'a_kept': len(s3_kept_customers & a_customers),
    'b_kept': len(s3_kept_customers & b_customers),
    'c_kept': len(s3_kept_customers & c_customers),
    'revenue': s3_revenue,
    'cogs': s3_cogs,
    'warehouse': s3_warehouse,
    'shipping': s3_shipping,
    'returns': s3_returns,
    'interest': s3_interest,
    'overhead': s3_overhead,
    'total_cost': s3_total_cost,
    'profit': s3_profit,
    'margin': s3_margin,
    'risk': 'MEDIUM-HIGH',
    'probability': 50,
    'timeline': '1-2 months',
    'recommendation': 'RISKY'
}
print(f"  ✓ Customers: {len(s3_kept_customers)}, Revenue: €{s3_revenue:,.0f}, Profit: €{s3_profit:,.0f}, Margin: {s3_margin:.2f}%")

# Scenario 4: Exit SMB only (keep Mid+Enterprise)
print("\n[SCENARIO 4] Exit SMB Only - Keep Mid-Market + Enterprise (294 customers)")
s4_customers = mid_customers | ent_customers
s4_orders = pnl_orders[pnl_orders['CustomerID'].isin(s4_customers)]
s4_revenue = s4_orders['TransactionAmount'].sum()
s4_cogs = s4_orders['COGS_EUR'].sum()
s4_warehouse = s4_orders['WarehouseCost_EUR'].sum()
s4_shipping = s4_orders['ShippingCost_EUR'].sum()
s4_returns = s4_orders['ReturnsCost_EUR'].sum()
s4_interest = s4_orders['InterestCost_EUR'].sum()
s4_overhead = s4_orders['OverheadCost_EUR'].sum() * 0.9  # Reduced overhead
s4_total_cost = s4_cogs + s4_warehouse + s4_shipping + s4_returns + s4_interest + s4_overhead
s4_profit = s4_revenue - s4_total_cost
s4_margin = (s4_profit / s4_revenue * 100) if s4_revenue > 0 else 0

scenarios['Exit SMB'] = {
    'customers_kept': len(s4_customers),
    'a_kept': len(s4_customers & a_customers),
    'b_kept': len(s4_customers & b_customers),
    'c_kept': len(s4_customers & c_customers),
    'revenue': s4_revenue,
    'cogs': s4_cogs,
    'warehouse': s4_warehouse,
    'shipping': s4_shipping,
    'returns': s4_returns,
    'interest': s4_interest,
    'overhead': s4_overhead,
    'total_cost': s4_total_cost,
    'profit': s4_profit,
    'margin': s4_margin,
    'risk': 'LOW-MEDIUM',
    'probability': 80,
    'timeline': '2-3 months',
    'recommendation': 'SAFE'
}
print(f"  ✓ Customers: {len(s4_customers)}, Revenue: €{s4_revenue:,.0f}, Profit: €{s4_profit:,.0f}, Margin: {s4_margin:.2f}%")

# Scenario 5: Enterprise only (keep Enterprise only)
print("\n[SCENARIO 5] Enterprise Only - Keep Enterprise customers only (66)")
s5_customers = ent_customers
s5_orders = pnl_orders[pnl_orders['CustomerID'].isin(s5_customers)]
s5_revenue = s5_orders['TransactionAmount'].sum()
s5_cogs = s5_orders['COGS_EUR'].sum()
s5_warehouse = s5_orders['WarehouseCost_EUR'].sum()
s5_shipping = s5_orders['ShippingCost_EUR'].sum()
s5_returns = s5_orders['ReturnsCost_EUR'].sum()
s5_interest = s5_orders['InterestCost_EUR'].sum()
s5_overhead = s5_orders['OverheadCost_EUR'].sum() * 0.5  # Highly reduced overhead
s5_total_cost = s5_cogs + s5_warehouse + s5_shipping + s5_returns + s5_interest + s5_overhead
s5_profit = s5_revenue - s5_total_cost
s5_margin = (s5_profit / s5_revenue * 100) if s5_revenue > 0 else 0

scenarios['Enterprise Only'] = {
    'customers_kept': len(s5_customers),
    'a_kept': len(s5_customers & a_customers),
    'b_kept': len(s5_customers & b_customers),
    'c_kept': len(s5_customers & c_customers),
    'revenue': s5_revenue,
    'cogs': s5_cogs,
    'warehouse': s5_warehouse,
    'shipping': s5_shipping,
    'returns': s5_returns,
    'interest': s5_interest,
    'overhead': s5_overhead,
    'total_cost': s5_total_cost,
    'profit': s5_profit,
    'margin': s5_margin,
    'risk': 'VERY HIGH',
    'probability': 25,
    'timeline': '6-12 months',
    'recommendation': 'EXTREME'
}
print(f"  ✓ Customers: {len(s5_customers)}, Revenue: €{s5_revenue:,.0f}, Profit: €{s5_profit:,.0f}, Margin: {s5_margin:.2f}%")

# Create summary DataFrame
print("\n[STEP 5] Creating scenario summary...")

scenarios_list = []
for scenario_name, metrics in scenarios.items():
    scenarios_list.append({
        'Scenario': scenario_name,
        'Customers_Kept': metrics['customers_kept'],
        'A_Customers': metrics['a_kept'],
        'B_Customers': metrics['b_kept'],
        'C_Customers': metrics['c_kept'],
        'Revenue_EUR': round(metrics['revenue'], 2),
        'COGS_EUR': round(metrics['cogs'], 2),
        'Warehouse_EUR': round(metrics['warehouse'], 2),
        'Shipping_EUR': round(metrics['shipping'], 2),
        'Returns_EUR': round(metrics['returns'], 2),
        'Interest_EUR': round(metrics['interest'], 2),
        'Overhead_EUR': round(metrics['overhead'], 2),
        'TotalCost_EUR': round(metrics['total_cost'], 2),
        'Profit_EUR': round(metrics['profit'], 2),
        'Margin_Pct': round(metrics['margin'], 2),
        'Risk_Level': metrics['risk'],
        'Success_Probability_Pct': metrics['probability'],
        'Timeline': metrics['timeline'],
        'Recommendation': metrics['recommendation']
    })

scenarios_df = pd.DataFrame(scenarios_list)

# Save files
print("\n[STEP 6] Saving scenarios...")

scenarios_df.to_csv('data/generated/14_scenario_planning.csv', index=False)
print(f"✓ Saved: 14_scenario_planning.csv")

# Print summary
print("\n" + "=" * 100)
print("DATASET 14 SCENARIO PLANNING SUMMARY")
print("=" * 100)

print("\n[SCENARIO COMPARISON]:")
for col in ['Scenario', 'Customers_Kept', 'Profit_EUR', 'Margin_Pct', 'Risk_Level', 'Recommendation']:
    print(f"{col}", end=" | ")
print()
for _, row in scenarios_df.iterrows():
    print(f"{row['Scenario']:20} | {row['Customers_Kept']:2} | €{row['Profit_EUR']:>10,.0f} | {row['Margin_Pct']:6.2f}% | {row['Risk_Level']:13} | {row['Recommendation']}")

print("\n" + "=" * 100)
print("✓ DATASET 14 GENERATION COMPLETE")
print("=" * 100)

