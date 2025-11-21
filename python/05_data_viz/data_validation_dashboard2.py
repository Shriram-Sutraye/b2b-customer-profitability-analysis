# data_validation_dashboard2.py
import pandas as pd

# Load scenario and cost data
scenario_df = pd.read_csv("../../data/generated/14_scenario_planning.csv")
fin_df = pd.read_csv("../../data/generated/10_financial_p_l_orders.csv")

print("="*80)
print("SECTION 1: STRATEGIC SCENARIO COMPARISON")
print("="*80)

# Scenario Table
print(scenario_df[["Scenario", "Revenue_EUR", "TotalCost_EUR", "Profit_EUR"]])

print("="*80)
print("SECTION 2: COST-TO-SERVE BREAKDOWN BY SEGMENT")
print("="*80)

segment_costs = fin_df.groupby("CLVSegment")[["COGS_EUR","WarehouseCost_EUR","ShippingCost_EUR","ReturnsCost_EUR","InterestCost_EUR","OverheadCost_EUR"]].sum()
print(segment_costs)

print("="*80)
print("SECTION 3: PROFIT BRIDGE (WATERFALL VALUES)")
print("="*80)

total_revenue = fin_df["TransactionAmount"].sum()
total_cogs = fin_df["COGS_EUR"].sum()
total_returns = fin_df["ReturnsCost_EUR"].sum()
total_shipping = fin_df["ShippingCost_EUR"].sum()
total_interest = fin_df["InterestCost_EUR"].sum()
total_overhead = fin_df["OverheadCost_EUR"].sum()
total_profit = fin_df["Profit_EUR"].sum()

print(f"Revenue:      {total_revenue:,.2f}")
print(f" - COGS:      {total_cogs:,.2f}")
print(f" - Returns:   {total_returns:,.2f}")
print(f" - Shipping:  {total_shipping:,.2f}")
print(f" - Interest:  {total_interest:,.2f}")
print(f" - Overhead:  {total_overhead:,.2f}")
print(f"= Profit:     {total_profit:,.2f}")

print("="*80)
print("SECTION 4: PRODUCT VS SEGMENT HEATMAP PREP")
print("="*80)

# Load product data & join if needed
try:
    prod_df = pd.read_csv("../../data/generated/products.csv")
    heatmap_df = fin_df.merge(prod_df[["ProductID","ProductCategory"]], on="ProductID", how="left")
    matrix = heatmap_df.groupby(["ProductCategory", "CLVSegment"])["Profit_EUR"].sum().unstack(fill_value=0)
    print(matrix)
except Exception as e:
    print("No product-level data found or join error:", str(e))

print("="*80)
print("SECTION 5: BEST-ACTION KPI (from scenarios)")
print("="*80)

# Show scenario with max Profit
best_row = scenario_df.iloc[scenario_df["Profit_EUR"].idxmax()]
print(f"Recommended Scenario: {best_row['Scenario']}, Expected Profit: {best_row['Profit_EUR']:,.2f} EUR")

print("="*80)
print("SECTION 6: PROFITABILITY GAUGE METRICS")
print("="*80)
# Current, Target, and Best-Scenario profit for gauge
current_profit = scenario_df.query("Scenario == 'Status Quo'")["Profit_EUR"].iloc[0]
target_profit = 500000  # Set your target value here
scenario_profit = best_row["Profit_EUR"]
print(f"Current: {current_profit:,.2f}, Target: {target_profit:,.2f}, Best Scenario: {scenario_profit:,.2f}")

print("="*80)
print("EOF")
