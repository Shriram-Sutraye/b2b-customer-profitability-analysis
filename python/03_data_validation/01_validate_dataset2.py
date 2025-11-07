import pandas as pd
import numpy as np
from datetime import datetime
import sys

print("=" * 100)
print("DATASET 2 COMPREHENSIVE VALIDATION & AUDIT")
print("Industry-Standard Data Quality Assessment")
print("=" * 100)

# Load data
print("\n[LOADING DATA]...")
try:
    transactions = pd.read_csv('data/generated/02_transactions_generated.csv')
    customers = pd.read_csv('data/processed/01_customer_master.csv')
    print(f"✓ Transactions: {len(transactions):,} rows × {len(transactions.columns)} columns")
    print(f"✓ Customers: {len(customers):,} rows")
except FileNotFoundError as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

# ============================================================================
# VALIDATION SUITE
# ============================================================================

validation_results = {
    'passed': [],
    'warnings': [],
    'failed': []
}

print("\n" + "=" * 100)
print("VALIDATION CHECKS")
print("=" * 100)

# ============================================================================
# 1. STRUCTURAL VALIDATION
# ============================================================================

print("\n[1] STRUCTURAL VALIDATION")
print("-" * 100)

# Check 1.1: Required columns
required_columns = [
    'TransactionID', 'CustomerID', 'TransactionDate', 'OrderMonth',
    'OrderDayOfWeek', 'ProductCategory', 'TransactionAmount', 'Quantity',
    'NumberOfLineItems', 'IsStandardOrder', 'IsUrgent',
    'CustomerServiceInteractionRequired', 'OrderIntensityLevel', 'ServiceCostMultiplier'
]

missing_cols = [col for col in required_columns if col not in transactions.columns]
if not missing_cols:
    print("  ✓ [1.1] All required columns present")
    validation_results['passed'].append("All required columns present")
else:
    print(f"  ✗ [1.1] Missing columns: {missing_cols}")
    validation_results['failed'].append(f"Missing columns: {missing_cols}")

# Check 1.2: Data types
print("  [1.2] Data type validation:")
type_checks = {
    'TransactionID': 'object',
    'CustomerID': 'object',
    'TransactionDate': 'object',
    'OrderMonth': 'int64',
    'TransactionAmount': 'float64',
    'Quantity': 'int64',
    'IsStandardOrder': 'bool',
    'IsUrgent': 'bool',
    'ServiceCostMultiplier': 'float64'
}

type_issues = []
for col, expected_type in type_checks.items():
    if col in transactions.columns:
        actual_type = str(transactions[col].dtype)
        if actual_type != expected_type:
            type_issues.append(f"  {col}: {actual_type} (expected {expected_type})")

if not type_issues:
    print("    ✓ All data types correct")
    validation_results['passed'].append("Data types validation passed")
else:
    print("    ⚠ Type warnings:")
    for issue in type_issues:
        print(f"    {issue}")
    validation_results['warnings'].append("Some data types differ from expected")

# ============================================================================
# 2. DATA COMPLETENESS
# ============================================================================

print("\n[2] DATA COMPLETENESS")
print("-" * 100)

# Check 2.1: No null values in critical fields
null_critical = transactions[required_columns].isnull().sum()
null_critical = null_critical[null_critical > 0]

if len(null_critical) == 0:
    print("  ✓ [2.1] No null values in critical fields")
    validation_results['passed'].append("No null values in critical fields")
else:
    print(f"  ✗ [2.1] Null values found:")
    for col, count in null_critical.items():
        print(f"    {col}: {count} nulls ({count/len(transactions)*100:.2f}%)")
    validation_results['failed'].append(f"Null values in critical fields: {null_critical.to_dict()}")

# Check 2.2: TransactionID uniqueness
if transactions['TransactionID'].nunique() == len(transactions):
    print("  ✓ [2.2] All TransactionIDs are unique")
    validation_results['passed'].append("TransactionIDs are unique")
else:
    duplicates = len(transactions) - transactions['TransactionID'].nunique()
    print(f"  ✗ [2.2] Found {duplicates} duplicate TransactionIDs")
    validation_results['failed'].append(f"Duplicate TransactionIDs: {duplicates}")

# ============================================================================
# 3. INDUSTRY STANDARDS VALIDATION
# ============================================================================

print("\n[3] INDUSTRY STANDARDS VALIDATION")
print("-" * 100)

# Check 3.1: Custom Order Rate by Channel
print("  [3.1] Custom Order Rate (Industry: HORECA 38%, Retail 7%):")
for channel in [1, 2]:
    channel_customers = customers[customers['OriginalChannel'] == channel]['CustomerID'].tolist()
    channel_trans = transactions[transactions['CustomerID'].isin(channel_customers)]
    
    custom_rate = (1 - channel_trans['IsStandardOrder'].mean()) * 100
    channel_name = "HORECA" if channel == 1 else "Retail"
    expected_rate = 38 if channel == 1 else 7
    tolerance = 2  # ±2%
    
    if abs(custom_rate - expected_rate) <= tolerance:
        print(f"    ✓ {channel_name}: {custom_rate:.1f}% (expected ~{expected_rate}%, tolerance ±{tolerance}%)")
        validation_results['passed'].append(f"{channel_name} custom rate within tolerance")
    else:
        print(f"    ⚠ {channel_name}: {custom_rate:.1f}% (expected ~{expected_rate}%, deviation {abs(custom_rate - expected_rate):.1f}%)")
        validation_results['warnings'].append(f"{channel_name} custom rate deviates by {abs(custom_rate - expected_rate):.1f}%")

# Check 3.2: Rush Order Rate by Channel
print("  [3.2] Rush Order Rate (Industry: HORECA 12%, Retail 4%):")
for channel in [1, 2]:
    channel_customers = customers[customers['OriginalChannel'] == channel]['CustomerID'].tolist()
    channel_trans = transactions[transactions['CustomerID'].isin(channel_customers)]
    
    rush_rate = channel_trans['IsUrgent'].mean() * 100
    channel_name = "HORECA" if channel == 1 else "Retail"
    expected_rate = 12 if channel == 1 else 4
    tolerance = 2  # ±2%
    
    if abs(rush_rate - expected_rate) <= tolerance:
        print(f"    ✓ {channel_name}: {rush_rate:.1f}% (expected ~{expected_rate}%, tolerance ±{tolerance}%)")
        validation_results['passed'].append(f"{channel_name} rush rate within tolerance")
    else:
        print(f"    ⚠ {channel_name}: {rush_rate:.1f}% (expected ~{expected_rate}%, deviation {abs(rush_rate - expected_rate):.1f}%)")
        validation_results['warnings'].append(f"{channel_name} rush rate deviates by {abs(rush_rate - expected_rate):.1f}%")

# Check 3.3: Service Cost Multiplier Range (1.0 - 1.8x)
print("  [3.3] Service Cost Multiplier Range (Industry: 1.0x - 1.8x):")
min_mult = transactions['ServiceCostMultiplier'].min()
max_mult = transactions['ServiceCostMultiplier'].max()

if min_mult >= 1.0 and max_mult <= 1.8:
    print(f"    ✓ Multiplier range: {min_mult:.2f}x - {max_mult:.2f}x (within 1.0-1.8x)")
    validation_results['passed'].append("Cost multiplier within range")
else:
    print(f"    ✗ Multiplier range: {min_mult:.2f}x - {max_mult:.2f}x (exceeds 1.0-1.8x limits)")
    validation_results['failed'].append(f"Cost multiplier out of range: min={min_mult:.2f}x, max={max_mult:.2f}x")

# Check 3.4: Order Intensity Distribution
print("  [3.4] Order Intensity Level Distribution:")
intensity_dist = transactions['OrderIntensityLevel'].value_counts(normalize=True) * 100
for level in ['Low', 'Medium', 'High']:
    pct = intensity_dist.get(level, 0)
    print(f"    {level}: {pct:.1f}%")
validation_results['passed'].append("Order intensity distribution calculated")

# ============================================================================
# 4. FINANCIAL VALIDATION
# ============================================================================

print("\n[4] FINANCIAL VALIDATION (CRITICAL)")
print("-" * 100)

# Check 4.1: Revenue Aggregation (±5% tolerance per customer)
print("  [4.1] Revenue Aggregation per Customer (Tolerance: ±5%):")
revenue_issues = []
total_variance = 0
customers_within_tolerance = 0

for customer_id in transactions['CustomerID'].unique():
    trans_total = transactions[transactions['CustomerID'] == customer_id]['TransactionAmount'].sum()
    expected = customers[customers['CustomerID'] == customer_id]['TotalAnnualRevenue'].values
    
    if len(expected) > 0:
        expected_val = expected[0]
        variance_pct = abs(trans_total - expected_val) / expected_val * 100
        total_variance += variance_pct
        
        if variance_pct <= 5:
            customers_within_tolerance += 1
        else:
            revenue_issues.append({
                'customer': customer_id,
                'generated': trans_total,
                'expected': expected_val,
                'variance_pct': variance_pct
            })

within_pct = (customers_within_tolerance / len(transactions['CustomerID'].unique())) * 100
avg_variance = total_variance / len(transactions['CustomerID'].unique())

if customers_within_tolerance / len(transactions['CustomerID'].unique()) >= 0.95:  # 95% within tolerance
    print(f"    ✓ {customers_within_tolerance}/{len(transactions['CustomerID'].unique())} customers within ±5% ({within_pct:.1f}%)")
    print(f"      Average variance: {avg_variance:.2f}%")
    validation_results['passed'].append(f"Revenue aggregation validated: {within_pct:.1f}% customers within tolerance")
else:
    print(f"    ✗ Only {customers_within_tolerance}/{len(transactions['CustomerID'].unique())} customers within ±5% ({within_pct:.1f}%)")
    print(f"      Average variance: {avg_variance:.2f}%")
    print(f"      Worst offenders (showing first 5):")
    for issue in sorted(revenue_issues, key=lambda x: x['variance_pct'], reverse=True)[:5]:
        print(f"        {issue['customer']}: Generated €{issue['generated']:.2f}, Expected €{issue['expected']:.2f} (Variance: {issue['variance_pct']:.2f}%)")
    validation_results['failed'].append(f"Revenue aggregation failed: only {within_pct:.1f}% within tolerance")

# Check 4.2: Transaction Amount Bounds
print("  [4.2] Transaction Amount Bounds (Industry: €40-1500 per order):")
min_amount = transactions['TransactionAmount'].min()
max_amount = transactions['TransactionAmount'].max()
avg_amount = transactions['TransactionAmount'].mean()

below_min = (transactions['TransactionAmount'] < 40).sum()
above_max = (transactions['TransactionAmount'] > 1500).sum()

if below_min == 0 and above_max == 0:
    print(f"    ✓ All amounts within €40-€1500 range")
    print(f"      Min: €{min_amount:.2f}, Avg: €{avg_amount:.2f}, Max: €{max_amount:.2f}")
    validation_results['passed'].append("Transaction amounts within bounds")
else:
    print(f"    ✗ Amounts outside bounds:")
    print(f"      Below €40: {below_min} ({below_min/len(transactions)*100:.2f}%)")
    print(f"      Above €1500: {above_max} ({above_max/len(transactions)*100:.2f}%)")
    validation_results['failed'].append(f"Transaction amounts out of bounds: {below_min} below min, {above_max} above max")

# ============================================================================
# 5. SEASONAL VALIDATION
# ============================================================================

print("\n[5] SEASONAL DISTRIBUTION")
print("-" * 100)

print("  [5.1] Monthly Distribution (Target: Jan -12% to Dec +40%):")
seasonal_dist = transactions.groupby('OrderMonth').size()
monthly_avg = len(transactions) / 12

seasonal_targets = {
    1: -12, 2: -10, 3: -8, 4: 3, 5: 5, 6: 8,
    7: 25, 8: 22, 9: 15, 10: 20, 11: 35, 12: 40
}

for month in range(1, 13):
    count = seasonal_dist.get(month, 0)
    pct_diff = ((count / monthly_avg - 1) * 100) if monthly_avg > 0 else 0
    target = seasonal_targets[month]
    month_name = datetime(2023, month, 1).strftime('%b')
    
    # Allow ±5% tolerance
    if abs(pct_diff - target) <= 5:
        print(f"    ✓ {month_name}: {count:5d} orders ({pct_diff:+6.1f}% vs avg, target {target:+3d}%)")
    else:
        print(f"    ⚠ {month_name}: {count:5d} orders ({pct_diff:+6.1f}% vs avg, target {target:+3d}%, deviation {abs(pct_diff - target):.1f}%)")

validation_results['passed'].append("Seasonal distribution calculated")

# ============================================================================
# 6. LOGICAL CONSISTENCY
# ============================================================================

print("\n[6] LOGICAL CONSISTENCY CHECKS")
print("-" * 100)

# Check 6.1: OrderIntensityLevel matches flags
print("  [6.1] OrderIntensityLevel vs Flags Consistency:")
consistency_issues = 0

for idx, row in transactions.iterrows():
    flags_sum = sum([not row['IsStandardOrder'], row['IsUrgent'], row['CustomerServiceInteractionRequired']])
    
    expected_intensity = 'Low' if flags_sum == 0 else ('Medium' if flags_sum == 1 else 'High')
    
    if row['OrderIntensityLevel'] != expected_intensity:
        consistency_issues += 1

if consistency_issues == 0:
    print(f"    ✓ All OrderIntensityLevels match their flags (0 inconsistencies)")
    validation_results['passed'].append("OrderIntensityLevel consistency validated")
else:
    print(f"    ✗ Found {consistency_issues} inconsistencies between OrderIntensityLevel and flags")
    validation_results['failed'].append(f"OrderIntensityLevel inconsistencies: {consistency_issues}")

# Check 6.2: ServiceCostMultiplier matches flags
print("  [6.2] ServiceCostMultiplier Range Check:")
multiplier_issues = 0

for idx, row in transactions.iterrows():
    expected_min = 1.0
    expected_max = 1.8
    
    if row['ServiceCostMultiplier'] < expected_min or row['ServiceCostMultiplier'] > expected_max:
        multiplier_issues += 1

if multiplier_issues == 0:
    print(f"    ✓ All ServiceCostMultipliers within 1.0-1.8x range")
    validation_results['passed'].append("ServiceCostMultiplier validation passed")
else:
    print(f"    ✗ Found {multiplier_issues} multipliers outside 1.0-1.8x range")
    validation_results['failed'].append(f"ServiceCostMultiplier out of range: {multiplier_issues} instances")

# ============================================================================
# 7. SUMMARY REPORT
# ============================================================================

print("\n" + "=" * 100)
print("VALIDATION SUMMARY REPORT")
print("=" * 100)

print(f"\nTotal Records Validated: {len(transactions):,}")
print(f"From {transactions['CustomerID'].nunique()} unique customers")
print(f"Date Range: {transactions['TransactionDate'].min()} to {transactions['TransactionDate'].max()}")

print(f"\n✓ PASSED ({len(validation_results['passed'])} checks):")
for check in validation_results['passed']:
    print(f"  • {check}")

if validation_results['warnings']:
    print(f"\n⚠ WARNINGS ({len(validation_results['warnings'])} alerts):")
    for warning in validation_results['warnings']:
        print(f"  • {warning}")
else:
    print(f"\n⚠ WARNINGS: None")

if validation_results['failed']:
    print(f"\n✗ FAILED ({len(validation_results['failed'])} critical issues):")
    for failure in validation_results['failed']:
        print(f"  • {failure}")
else:
    print(f"\n✗ FAILED: None")

print("\n" + "=" * 100)
print("DATA QUALITY SCORE")
print("=" * 100)

total_checks = len(validation_results['passed']) + len(validation_results['warnings']) + len(validation_results['failed'])
quality_score = (len(validation_results['passed']) / total_checks * 100) if total_checks > 0 else 0

print(f"\nPassed: {len(validation_results['passed'])}/{total_checks} ({len(validation_results['passed'])/total_checks*100:.1f}%)")
print(f"Quality Score: {quality_score:.1f}%")

if quality_score >= 95:
    status = "✓ EXCELLENT - Ready for production"
elif quality_score >= 85:
    status = "✓ GOOD - Minor warnings, generally usable"
elif quality_score >= 70:
    status = "⚠ FAIR - Warnings present, address before use"
else:
    status = "✗ POOR - Critical issues, do not use"

print(f"Status: {status}")

print("\n" + "=" * 100)
print("VALIDATION COMPLETE")
print("=" * 100)

# Exit with appropriate code
sys.exit(0 if len(validation_results['failed']) == 0 else 1)

