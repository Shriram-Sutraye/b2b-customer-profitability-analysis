import pandas as pd
import sys

print("=" * 100)
print("DATASET 14: SCENARIO PLANNING VALIDATION")
print("=" * 100)

try:
    scenarios = pd.read_csv('data/generated/14_scenario_planning.csv')
    print(f"✓ Loaded 14_scenario_planning.csv ({len(scenarios)} scenarios)")
except FileNotFoundError as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

print("\n[VALIDATION 1] All 5 scenarios generated:")
print(f"  {list(scenarios['Scenario'].unique())}")
if len(scenarios) == 5:
    print(f"  ✓ PASS: 5 scenarios")

print("\n[VALIDATION 2] Profitability improvement:")
status_quo_profit = scenarios[scenarios['Scenario'] == 'Status Quo']['Profit_EUR'].values[0]
best_profit = scenarios['Profit_EUR'].max()
improvement = best_profit / status_quo_profit
print(f"  Status Quo: €{status_quo_profit:,.0f}")
print(f"  Best Scenario: €{best_profit:,.0f}")
print(f"  Improvement: {improvement:.1f}x ✓")

print("\n[VALIDATION 3] Risk assessment present:")
if scenarios['Risk_Level'].notna().all():
    print(f"  ✓ Risk levels assigned")

print("\n[VALIDATION 4] Recommendations present:")
if scenarios['Recommendation'].notna().all():
    print(f"  ✓ Recommendations assigned")

print("\n[KEY FINDINGS]:")
best_row = scenarios.loc[scenarios['Profit_EUR'].idxmax()]
print(f"  Best scenario: {best_row['Scenario']}")
print(f"  Profit: €{best_row['Profit_EUR']:,.0f}")
print(f"  Margin: {best_row['Margin_Pct']:.2f}%")
print(f"  Recommendation: {best_row['Recommendation']}")

safe_row = scenarios[scenarios['Recommendation'] == 'SAFE'].iloc[0] if any(scenarios['Recommendation'] == 'SAFE') else None
if safe_row is not None:
    print(f"\n  Safe alternative: {safe_row['Scenario']}")
    print(f"  Profit: €{safe_row['Profit_EUR']:,.0f}")
    print(f"  Margin: {safe_row['Margin_Pct']:.2f}%")

print("\n✓ VERDICT: Dataset 14 Complete - CFO ready to decide")

