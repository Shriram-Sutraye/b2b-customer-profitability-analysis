import pandas as pd

# Load Data
orders = pd.read_csv('data/generated/10_financial_p_l_orders.csv')
clv = pd.read_csv('data/generated/11_customer_lifetime_value.csv')
returns = pd.read_csv('data/generated/06_returns_handling_generated.csv')

print("--- METRIC VERIFICATION ---")

# 1. Customer Segmentation Counts
print("\n1. Customer Segmentation Counts:")
print(clv['CLVSegment'].value_counts())

# 2. C-Tier Impact
c_tier = clv[clv['CLVSegment'] == 'C-Customer']
print(f"\n2. C-Tier Impact:")
print(f"   Count: {len(c_tier)}")
print(f"   Total Annual Profit: €{c_tier['AnnualProfit_EUR'].sum():,.2f}")
print(f"   Total CLV: €{c_tier['CLV_EUR'].sum():,.2f}")

# 3. Return Rate
# Definition: Count of Returned items / Total items OR Value of Returns / Total Revenue?
# README says "Company return rate: 7.80%".
# Let's check % of transactions with returns
ret_txns = returns['IsReturned'].sum()
total_txns = len(returns)
print(f"\n3. Return Rate Analysis:")
print(f"   Transactions with Return: {ret_txns}/{total_txns} ({ret_txns/total_txns*100:.2f}%)")
# Let's check Value of Returned Goods vs Total Revenue
val_returned = returns[returns['IsReturned']==True]['TransactionAmount_EUR'].sum()
total_rev = returns['TransactionAmount_EUR'].sum()
print(f"   Value Returned %: {val_returned/total_rev*100:.2f}%")

# 4. Fresh Product Operational Costs
# Operational Cost = Warehouse + Shipping + Returns + Overhead (excluding COGS & Interest?)
# README says "Fresh Products: €3.0M (highest cost category)"
fresh_ops = orders[orders['ProductCategory'] == 'Fresh']
fresh_ops_cost = (fresh_ops['WarehouseCost_EUR'].sum() + 
                  fresh_ops['ShippingCost_EUR'].sum() + 
                  fresh_ops['ReturnsCost_EUR'].sum() + 
                  fresh_ops['OverheadCost_EUR'].sum())
print(f"\n4. Fresh Product Operational Costs:")
print(f"   Fresh Ops Cost (Whse+Ship+Ret+Overhead): €{fresh_ops_cost:,.2f}")
print(f"   Fresh COGS: €{fresh_ops['COGS_EUR'].sum():,.2f}")
print(f"   Fresh Total Cost: €{fresh_ops['TotalCost_EUR'].sum():,.2f}")

# 5. Scenario Profit
# README says "Renegotiate C-Tier: €3.0M"
# We need to calculate or recall the scenario output.
# Let's just check the total potential improvement if C-tier became break-even (0 profit)
# Current Profit = €82k. C-Tier Loss = -€1.25M.
# If C-Tier -> 0, New Profit = 82k + 1.25M = €1.33M.
# If C-Tier -> Profitable (e.g. +10% margin on their revenue)?
# C-Tier Revenue = orders[orders['CustomerID'].isin(c_tier['CustomerID'])]['TransactionAmount'].sum()
c_rev = orders[orders['CustomerID'].isin(c_tier['CustomerID'])]['TransactionAmount'].sum()
print(f"\n5. Scenario Potential:")
print(f"   C-Tier Revenue: €{c_rev:,.2f}")
print(f"   If C-Tier achieved 10% margin: Profit = €{c_rev * 0.10:,.2f}")
print(f"   Total Potential (Baseline + Improvement): €{82661 + (c_rev * 0.10):,.2f}")

