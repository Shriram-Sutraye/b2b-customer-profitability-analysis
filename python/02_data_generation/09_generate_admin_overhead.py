import pandas as pd
import numpy as np
import sys

print("=" * 100)
print("DATASET 9: ADMIN OVERHEAD ALLOCATION (INDUSTRY-STANDARD)")
print("Segment-weighted + Product-adjusted allocation")
print("=" * 100)

# Load data
print("\n[STEP 1] Loading dependent datasets...")
try:
    transactions = pd.read_csv('data/generated/02_transactions_generated.csv')
    customers = pd.read_csv('data/processed/01_customer_master.csv')
    print(f"✓ Loaded {len(transactions)} transactions")
    print(f"✓ Loaded {len(customers)} customers")
except FileNotFoundError as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

# Merge for customer segment
trans_with_segment = transactions.merge(customers[['CustomerID', 'CustomerSegment']], on='CustomerID')

# Admin overhead components (annual) - Real B2B food distributor estimate
print("\n[STEP 2] Defining overhead structure...")

overhead_components = {
    'Salaries_Management': 250000,      # CEO, CFO, VP Operations
    'Salaries_Finance': 150000,         # Accountants, billing staff
    'Salaries_Admin': 120000,           # HR, reception, general admin
    'Salaries_IT': 100000,              # IT support, systems
    'Rent_Facility': 180000,            # Warehouse office space
    'Utilities': 60000,                 # Electric, water, gas
    'Insurance': 80000,                 # General liability, property
    'Office_Equipment': 30000,          # Desks, furniture, maintenance
    'Software_Systems': 50000,          # ERP, accounting, CRM licenses
    'Professional_Services': 40000,     # Legal, audit, consulting
    'Marketing_Overhead': 70000,        # Brand, corporate marketing
    'Other': 50000                      # Miscellaneous
}

total_annual_overhead = sum(overhead_components.values())
print(f"✓ Total Annual Overhead: €{total_annual_overhead:,.2f}")

# Base overhead per transaction (equal split)
total_transactions = len(trans_with_segment)
base_overhead_per_transaction = total_annual_overhead / total_transactions

print(f"✓ Total Transactions/year: {total_transactions:,}")
print(f"✓ Base Overhead per Transaction: €{base_overhead_per_transaction:.2f}")

# Segment multipliers (based on support needs)
print("\n[STEP 3] Setting segment multipliers...")

segment_multipliers = {
    'SMB': 0.85,           # Less support, self-service
    'Mid-Market': 1.1,     # Standard service
    'Enterprise': 1.4      # Dedicated support, complexity
}

for segment, mult in segment_multipliers.items():
    calc_overhead = base_overhead_per_transaction * mult
    print(f"  {segment}: {mult}x multiplier = €{calc_overhead:.2f}/order")

# Product-based adjustments (based on handling complexity)
print("\n[STEP 4] Setting product adjustments...")

product_adjustments = {
    'Fresh': 10.00,         # Temperature control, perishability
    'Delicatessen': 8.00,   # Premium handling, spoilage risk
    'Milk': 5.00,           # Temperature control
    'Frozen': 0.00,         # Stable, no additional complexity
    'Grocery': -5.00,       # Simple, durable items
    'DetergentsPaper': -5.00 # Non-perishable, simple
}

for product, adj in product_adjustments.items():
    print(f"  {product}: {adj:+.2f} EUR adjustment")

# Generate overhead allocation
print("\n[STEP 5] Calculating overhead per transaction...")

overhead_data = []

for idx, trans in trans_with_segment.iterrows():
    transaction_id = trans['TransactionID']
    customer_id = trans['CustomerID']
    transaction_amount = trans['TransactionAmount']
    segment = trans['CustomerSegment']
    product_category = trans['ProductCategory']
    
    # Base overhead
    base_overhead = base_overhead_per_transaction
    
    # Segment multiplier
    segment_multiplier = segment_multipliers.get(segment, 1.0)
    segment_overhead = base_overhead * segment_multiplier
    
    # Product adjustment
    product_adjustment = product_adjustments.get(product_category, 0.00)
    
    # Total allocated overhead (but min €30 to ensure coverage)
    total_allocated_overhead = max(segment_overhead + product_adjustment, 30.00)
    
    # Create record
    overhead_record = {
        'TransactionID': transaction_id,
        'CustomerID': customer_id,
        'CustomerSegment': segment,
        'ProductCategory': product_category,
        'TransactionAmount_EUR': round(transaction_amount, 2),
        'BaseOverhead_EUR': round(base_overhead, 2),
        'SegmentMultiplier': segment_multiplier,
        'SegmentAdjustedOverhead_EUR': round(segment_overhead, 2),
        'ProductAdjustment_EUR': round(product_adjustment, 2),
        'TotalAllocatedOverhead_EUR': round(total_allocated_overhead, 2),
        'OverheadAsPercentOfRevenue': round((total_allocated_overhead / transaction_amount * 100), 2)
    }
    
    overhead_data.append(overhead_record)
    
    if (idx + 1) % 2000 == 0:
        print(f"  ✓ Processed {idx + 1}/{len(trans_with_segment)} transactions")

# Create DataFrame
print("\n[STEP 6] Creating DataFrame...")
overhead_df = pd.DataFrame(overhead_data)
print(f"✓ Generated {len(overhead_df)} overhead allocations")

# Validation
print("\n[STEP 7] Validation...")

print(f"\n  [7.1] Total Overhead Allocation:")
total_allocated = overhead_df['TotalAllocatedOverhead_EUR'].sum()
print(f"    Total: €{total_allocated:,.2f}")
print(f"    Expected: ~€{total_annual_overhead:,.2f}")
deviation = abs(total_allocated - total_annual_overhead) / total_annual_overhead * 100
print(f"    Deviation: {deviation:.1f}%")

print(f"\n  [7.2] Overhead by Segment:")
for segment in ['SMB', 'Mid-Market', 'Enterprise']:
    seg_data = overhead_df[overhead_df['CustomerSegment'] == segment]
    if len(seg_data) > 0:
        total = seg_data['TotalAllocatedOverhead_EUR'].sum()
        avg = seg_data['TotalAllocatedOverhead_EUR'].mean()
        count = len(seg_data)
        pct_of_total = (total / total_allocated) * 100
        print(f"    {segment}: {count:,} orders, €{avg:.2f} avg, €{total:,.2f} total ({pct_of_total:.1f}%)")

print(f"\n  [7.3] Overhead by Product Category:")
for category in overhead_df['ProductCategory'].unique():
    cat_data = overhead_df[overhead_df['ProductCategory'] == category]
    if len(cat_data) > 0:
        avg = cat_data['TotalAllocatedOverhead_EUR'].mean()
        count = len(cat_data)
        print(f"    {category}: {count:,} orders, €{avg:.2f} avg")

print(f"\n  [7.4] Overhead Statistics:")
print(f"    Minimum: €{overhead_df['TotalAllocatedOverhead_EUR'].min():.2f}")
print(f"    Average: €{overhead_df['TotalAllocatedOverhead_EUR'].mean():.2f}")
print(f"    Maximum: €{overhead_df['TotalAllocatedOverhead_EUR'].max():.2f}")

print(f"\n  [7.5] Overhead as % of Revenue:")
avg_pct = overhead_df['OverheadAsPercentOfRevenue'].mean()
print(f"    Average: {avg_pct:.2f}% of order value")
print(f"    Min: {overhead_df['OverheadAsPercentOfRevenue'].min():.2f}%")
print(f"    Max: {overhead_df['OverheadAsPercentOfRevenue'].max():.2f}%")

# Save to CSV
print("\n[STEP 8] Saving Dataset 9...")
output_file = 'data/generated/09_admin_overhead_generated.csv'
overhead_df.to_csv(output_file, index=False)
print(f"✓ Saved to {output_file}")

# Summary
print("\n" + "=" * 100)
print("DATASET 9 GENERATION SUMMARY")
print("=" * 100)

print(f"\nAdmin Overhead Allocation (Industry-Standard Hybrid):")
print(f"  Total Annual Overhead: €{total_annual_overhead:,.2f}")
print(f"  Total Transactions: {len(overhead_df):,}")
print(f"  Average Overhead per Order: €{overhead_df['TotalAllocatedOverhead_EUR'].mean():.2f}")
print(f"  Total Allocated: €{overhead_df['TotalAllocatedOverhead_EUR'].sum():,.2f}")

print(f"\nOverhead Components (Annual):")
for component, amount in overhead_components.items():
    pct = (amount / total_annual_overhead) * 100
    print(f"  {component}: €{amount:,} ({pct:.1f}%)")

print(f"\nAllocation by Segment:")
for segment, mult in segment_multipliers.items():
    seg_data = overhead_df[overhead_df['CustomerSegment'] == segment]
    if len(seg_data) > 0:
        avg = seg_data['TotalAllocatedOverhead_EUR'].mean()
        total = seg_data['TotalAllocatedOverhead_EUR'].sum()
        print(f"  {segment}: €{avg:.2f}/order avg, €{total:,.2f} total ({mult}x multiplier)")

print(f"\nAllocation by Product Category:")
for category in sorted(overhead_df['ProductCategory'].unique()):
    cat_data = overhead_df[overhead_df['ProductCategory'] == category]
    if len(cat_data) > 0:
        avg = cat_data['TotalAllocatedOverhead_EUR'].mean()
        adj = product_adjustments.get(category, 0)
        print(f"  {category}: €{avg:.2f}/order ({adj:+.2f} adjustment)")

print(f"\nKey Insights:")
print(f"  ✓ Industry-standard hybrid approach (segment + product)")
print(f"  ✓ Enterprise customers cost {segment_multipliers['Enterprise']/segment_multipliers['SMB']:.2f}x more overhead than SMB")
print(f"  ✓ Fresh products cost €{product_adjustments['Fresh']:.2f} more due to temperature control")
print(f"  ✓ Average overhead: {avg_pct:.2f}% of revenue")

print("\n" + "=" * 100)
print("✓ DATASET 9 GENERATION COMPLETE")
print("=" * 100)

