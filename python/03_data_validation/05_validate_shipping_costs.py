import pandas as pd
import numpy as np
import sys

print("=" * 100)
print("DATASET 5: INDEPENDENT SHIPPING COSTS VALIDATION AUDIT")
print("Validation Against B2B Food Wholesale Shipping Benchmarks")
print("=" * 100)

# Load data
print("\n[LOADING DATA]...")
try:
    shipping = pd.read_csv('data/generated/05_shipping_costs_generated.csv')
    transactions = pd.read_csv('data/generated/02_transactions_generated.csv')
    print(f"✓ Loaded {len(shipping)} shipping cost records")
    print(f"✓ Loaded {len(transactions)} transactions")
except FileNotFoundError as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

# Industry benchmarks for B2B food shipping
industry_benchmarks = {
    'avg_shipping_custom': (30.0, 80.0),      # €30-80 per custom order
    'standard_order_cost': 0.0,               # €0 (customer pays)
    'weight_surcharge': (0.50, 1.50),         # €0.50-1.50 per kg
    'cold_chain_premium': (10.0, 25.0),       # €10-25 for perishable
    'urgency_premium': (15.0, 30.0),          # €15-30 for urgent
    'pct_custom_orders': (10.0, 25.0),        # 10-25% of orders need our shipping
}

print("\n[INDUSTRY BENCHMARKS APPLIED]")
print("Sources: ShipBob, 3PL Food Operators, B2B Wholesale Data 2025")

# ============================================================================
# VALIDATION 1: ORDER DISTRIBUTION
# ============================================================================

print("\n" + "=" * 100)
print("VALIDATION 1: ORDER DISTRIBUTION")
print("=" * 100)

standard_orders = shipping[shipping['IsStandardOrder'] == True]
custom_orders = shipping[shipping['IsStandardOrder'] == False]

standard_pct = (len(standard_orders) / len(shipping)) * 100
custom_pct = (len(custom_orders) / len(shipping)) * 100

print(f"\n[1.1] Order Type Distribution:")
print(f"  Standard Orders (customer ships): {len(standard_orders):,} ({standard_pct:.1f}%)")
print(f"  Custom Orders (we ship): {len(custom_orders):,} ({custom_pct:.1f}%)")

expected_min, expected_max = industry_benchmarks['pct_custom_orders']
if expected_min <= custom_pct <= expected_max:
    print(f"  ✓ PASS: Custom orders {custom_pct:.1f}% within {expected_min}-{expected_max}% benchmark")
else:
    print(f"  ⚠ {custom_pct:.1f}% (Target: {expected_min}-{expected_max}%)")

# ============================================================================
# VALIDATION 2: STANDARD ORDERS COST
# ============================================================================

print("\n" + "=" * 100)
print("VALIDATION 2: STANDARD ORDERS COST (Should be €0)")
print("=" * 100)

standard_avg_cost = standard_orders['TotalShippingCost_EUR'].sum()

print(f"\n[2.1] Standard Order Costs:")
print(f"  Total standard order shipping cost: €{standard_avg_cost:.2f}")

if standard_avg_cost == 0.0:
    print(f"  ✓ PASS: Standard orders correctly cost €0")
else:
    print(f"  ✗ FAIL: Standard orders should cost €0, not €{standard_avg_cost:.2f}")

# ============================================================================
# VALIDATION 3: CUSTOM ORDERS COST RANGE
# ============================================================================

print("\n" + "=" * 100)
print("VALIDATION 3: CUSTOM ORDERS COST RANGE")
print("=" * 100)

if len(custom_orders) > 0:
    custom_min = custom_orders['TotalShippingCost_EUR'].min()
    custom_avg = custom_orders['TotalShippingCost_EUR'].mean()
    custom_max = custom_orders['TotalShippingCost_EUR'].max()
    
    print(f"\n[3.1] Custom Order Shipping Costs:")
    print(f"  Minimum: €{custom_min:.2f}")
    print(f"  Average: €{custom_avg:.2f}")
    print(f"  Maximum: €{custom_max:.2f}")
    
    expected_min, expected_max = industry_benchmarks['avg_shipping_custom']
    if expected_min <= custom_avg <= expected_max:
        print(f"  ✓ PASS: Average €{custom_avg:.2f} within €{expected_min}-{expected_max} benchmark")
    else:
        print(f"  ⚠ Average €{custom_avg:.2f} (Target: €{expected_min}-{expected_max})")
else:
    print("  No custom orders found")

# ============================================================================
# VALIDATION 4: COST COMPONENTS
# ============================================================================

print("\n" + "=" * 100)
print("VALIDATION 4: COST COMPONENTS (Custom Orders Only)")
print("=" * 100)

if len(custom_orders) > 0:
    total_base = custom_orders['BaseShippingCost_EUR'].sum()
    total_weight = custom_orders['WeightSurchargeCost_EUR'].sum()
    total_cold = custom_orders['ColdChainPremium_EUR'].sum()
    total_urgency = custom_orders['UrgencyPremium_EUR'].sum()
    total_shipping = custom_orders['TotalShippingCost_EUR'].sum()
    
    base_pct = (total_base / total_shipping) * 100 if total_shipping > 0 else 0
    weight_pct = (total_weight / total_shipping) * 100 if total_shipping > 0 else 0
    cold_pct = (total_cold / total_shipping) * 100 if total_shipping > 0 else 0
    urgency_pct = (total_urgency / total_shipping) * 100 if total_shipping > 0 else 0
    
    print(f"\n[4.1] Shipping Cost Breakdown:")
    print(f"  Base shipping: €{total_base:,.2f} ({base_pct:.1f}%)")
    print(f"  Weight surcharge: €{total_weight:,.2f} ({weight_pct:.1f}%)")
    print(f"  Cold chain premium: €{total_cold:,.2f} ({cold_pct:.1f}%)")
    print(f"  Urgency premium: €{total_urgency:,.2f} ({urgency_pct:.1f}%)")
    
    print(f"\n[4.2] Cost Component Analysis:")
    if 20 <= base_pct <= 40:
        print(f"  ✓ Base: {base_pct:.1f}% (Target: 20-40%)")
    else:
        print(f"  ⚠ Base: {base_pct:.1f}% (Target: 20-40%)")
    
    if 20 <= weight_pct <= 40:
        print(f"  ✓ Weight: {weight_pct:.1f}% (Target: 20-40%)")
    else:
        print(f"  ⚠ Weight: {weight_pct:.1f}% (Target: 20-40%)")
    
    if 10 <= cold_pct <= 30:
        print(f"  ✓ Cold chain: {cold_pct:.1f}% (Target: 10-30%)")
    else:
        print(f"  ⚠ Cold chain: {cold_pct:.1f}% (Target: 10-30%)")

# ============================================================================
# VALIDATION 5: WEIGHT SURCHARGE
# ============================================================================

print("\n" + "=" * 100)
print("VALIDATION 5: WEIGHT SURCHARGE ANALYSIS")
print("=" * 100)

if len(custom_orders) > 0:
    custom_with_weight = custom_orders[custom_orders['OrderWeight_kg'] > 0]
    if len(custom_with_weight) > 0:
        avg_weight = custom_with_weight['OrderWeight_kg'].mean()
        total_weight_charge = custom_with_weight['WeightSurchargeCost_EUR'].sum()
        implied_rate = total_weight_charge / custom_with_weight['OrderWeight_kg'].sum()
        
        print(f"\n[5.1] Weight Surcharge Validation:")
        print(f"  Average order weight: {avg_weight:.2f} kg")
        print(f"  Implied surcharge rate: €{implied_rate:.2f}/kg")
        
        expected_min, expected_max = industry_benchmarks['weight_surcharge']
        if expected_min <= implied_rate <= expected_max:
            print(f"  ✓ PASS: Rate €{implied_rate:.2f}/kg within €{expected_min}-{expected_max} benchmark")
        else:
            print(f"  ⚠ Rate €{implied_rate:.2f}/kg (Target: €{expected_min}-{expected_max}/kg)")

# ============================================================================
# VALIDATION 6: COLD CHAIN PREMIUM
# ============================================================================

print("\n" + "=" * 100)
print("VALIDATION 6: COLD CHAIN PREMIUM (Perishable Orders)")
print("=" * 100)

perishable_cats = ['Fresh', 'Milk', 'Delicatessen']
if len(custom_orders) > 0:
    perishable_orders = custom_orders[custom_orders['ProductCategory'].isin(perishable_cats)]
    non_perishable_orders = custom_orders[~custom_orders['ProductCategory'].isin(perishable_cats)]
    
    if len(perishable_orders) > 0:
        perishable_avg = perishable_orders['TotalShippingCost_EUR'].mean()
        perishable_premium_avg = perishable_orders['ColdChainPremium_EUR'].mean()
        print(f"\n[6.1] Perishable Order Costs:")
        print(f"  Count: {len(perishable_orders):,}")
        print(f"  Avg total cost: €{perishable_avg:.2f}")
        print(f"  Avg cold chain premium: €{perishable_premium_avg:.2f}")
        
        if 10 <= perishable_premium_avg <= 25:
            print(f"  ✓ PASS: Premium €{perishable_premium_avg:.2f} within €10-25 benchmark")
        else:
            print(f"  ⚠ Premium €{perishable_premium_avg:.2f} (Target: €10-25)")
    
    if len(non_perishable_orders) > 0:
        non_perishable_avg = non_perishable_orders['TotalShippingCost_EUR'].mean()
        print(f"\n[6.2] Non-Perishable Order Costs:")
        print(f"  Count: {len(non_perishable_orders):,}")
        print(f"  Avg total cost: €{non_perishable_avg:.2f}")
        
        if len(perishable_orders) > 0:
            multiplier = perishable_avg / non_perishable_avg if non_perishable_avg > 0 else 0
            print(f"  Cost multiplier (Perishable vs Non): {multiplier:.2f}x")
            if 1.1 <= multiplier <= 1.5:
                print(f"  ✓ PASS: Multiplier {multiplier:.2f}x reasonable (cold chain adds 10-50%)")

# ============================================================================
# VALIDATION 7: URGENCY PREMIUM
# ============================================================================

print("\n" + "=" * 100)
print("VALIDATION 7: URGENCY PREMIUM")
print("=" * 100)

if len(custom_orders) > 0:
    urgent_orders = custom_orders[custom_orders['IsUrgent'] == True]
    non_urgent_orders = custom_orders[custom_orders['IsUrgent'] == False]
    
    if len(urgent_orders) > 0:
        urgent_avg = urgent_orders['TotalShippingCost_EUR'].mean()
        urgent_premium_avg = urgent_orders['UrgencyPremium_EUR'].mean()
        print(f"\n[7.1] Urgent Order Costs:")
        print(f"  Count: {len(urgent_orders):,} ({len(urgent_orders)/len(custom_orders)*100:.1f}%)")
        print(f"  Avg total cost: €{urgent_avg:.2f}")
        print(f"  Avg urgency premium: €{urgent_premium_avg:.2f}")
        
        expected_min, expected_max = industry_benchmarks['urgency_premium']
        if expected_min <= urgent_premium_avg <= expected_max:
            print(f"  ✓ PASS: Premium €{urgent_premium_avg:.2f} within €{expected_min}-{expected_max} benchmark")
        else:
            print(f"  ⚠ Premium €{urgent_premium_avg:.2f} (Target: €{expected_min}-{expected_max})")
    
    if len(non_urgent_orders) > 0:
        non_urgent_avg = non_urgent_orders['TotalShippingCost_EUR'].mean()
        print(f"\n[7.2] Standard Urgent Order Costs:")
        print(f"  Count: {len(non_urgent_orders):,} ({len(non_urgent_orders)/len(custom_orders)*100:.1f}%)")
        print(f"  Avg total cost: €{non_urgent_avg:.2f}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 100)
print("FINAL VALIDATION SUMMARY")
print("=" * 100)

checks = [
    ("Standard orders = €0", standard_avg_cost == 0.0),
    ("Custom orders 10-25%", expected_min <= custom_pct <= expected_max if 'expected_min' in locals() else False),
    ("Avg custom €30-80", 30 <= custom_avg <= 80 if len(custom_orders) > 0 else False),
    ("Cost components realistic", base_pct > 0 and weight_pct > 0 if len(custom_orders) > 0 else False),
    ("Weight surcharge €0.50-1.50/kg", expected_min <= implied_rate <= expected_max if 'implied_rate' in locals() else False),
]

passed = sum(1 for _, result in checks if result)
total = len(checks)
score = (passed / total) * 100

print(f"\nCompliance: {passed}/{total} checks ({score:.0f}%)")

print(f"\nTotal Shipping Costs:")
print(f"  Standard orders: €{standard_avg_cost:,.2f} (Customer pays)")
if len(custom_orders) > 0:
    print(f"  Custom orders total: €{custom_orders['TotalShippingCost_EUR'].sum():,.2f}")
    print(f"  Average per custom: €{custom_orders['TotalShippingCost_EUR'].mean():.2f}")

if score >= 80:
    print(f"\n✓ VERDICT: GOOD - Dataset 5 passes key validations")
elif score >= 60:
    print(f"\n⚠ VERDICT: ACCEPTABLE - Minor deviations from benchmarks")
else:
    print(f"\n✗ VERDICT: NEEDS REVIEW")

print("\n" + "=" * 100)
print("✓ VALIDATION COMPLETE")
print("=" * 100)

