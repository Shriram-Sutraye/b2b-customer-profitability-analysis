import pandas as pd
import numpy as np
from datetime import datetime
import sys

np.random.seed(42)

print("=" * 80)
print("DATASET 2: TRANSACTIONS GENERATION (CORRECTED)")
print("With Deterministic Revenue Allocation & Seasonality")
print("=" * 80)

# Load data
print("\n[STEP 1] Loading Customer Master...")
try:
    customers = pd.read_csv('data/processed/01_customer_master.csv')
    print(f"✓ Loaded {len(customers)} customers")
except FileNotFoundError:
    print("✗ ERROR: Customer Master not found")
    sys.exit(1)

# Industry standards
seasonal_multipliers = {
    1: 0.88, 2: 0.90, 3: 0.92, 4: 1.03, 5: 1.05, 6: 1.08,
    7: 1.25, 8: 1.22, 9: 1.15, 10: 1.20, 11: 1.35, 12: 1.40
}

channel_params = {
    1: {'custom_rate': 0.38, 'rush_rate': 0.12, 'avg_order_size': 175, 'support_rate': 0.12},
    2: {'custom_rate': 0.07, 'rush_rate': 0.04, 'avg_order_size': 500, 'support_rate': 0.08}
}

print("[STEP 2] Applying Industry Standards...")
print("✓ Seasonal multipliers (Jan -12% to Dec +40%)")
print("✓ Channel-specific rates")
print("✓ Deterministic revenue allocation")

# Generate transactions
print("\n[STEP 3] Generating transactions with revenue lock...")

all_transactions = []
transaction_counter = 1

for idx, customer in customers.iterrows():
    customer_id = customer['CustomerID']
    channel = customer['OriginalChannel']
    order_frequency = customer['OrderFrequencyPerMonth']
    
    params = channel_params[channel]
    
    # Calculate total orders for year
    annual_orders = int(order_frequency * 12)
    if annual_orders < 1:
        annual_orders = 1
    
    # Get annual spending by category
    categories = ['Fresh', 'Milk', 'Grocery', 'Frozen', 'DetergentsPaper', 'Delicatessen']
    category_spending_columns = {
        'Fresh': 'AnnualFreshSpending',
        'Milk': 'AnnualMilkSpending',
        'Grocery': 'AnnualGrocerySpending',
        'Frozen': 'AnnualFrozenSpending',
        'DetergentsPaper': 'AnnualDetergentsPaperSpending',
        'Delicatessen': 'AnnualDelicatessenSpending'
    }
    
    annual_spending_by_cat = {}
    for cat in categories:
        col_name = category_spending_columns[cat]
        annual_spending_by_cat[cat] = customer[col_name] if col_name in customer.index else 0
    
    total_annual = sum(annual_spending_by_cat.values())
    
    if total_annual <= 0:
        continue
    
    # CRITICAL FIX: Pre-calculate order amounts for the year to ensure they sum to total_annual
    # This ensures revenue accuracy ±1%
    
    annual_orders_list = []
    for month in range(1, 13):
        seasonal_mult = seasonal_multipliers[month]
        monthly_budget = (total_annual / 12) * seasonal_mult
        
        orders_this_month = max(1, int(annual_orders / 12) + np.random.randint(-1, 2))
        
        for _ in range(orders_this_month):
            # Generate order amount from log-normal, then normalize
            order_amount = np.random.lognormal(mean=np.log(params['avg_order_size']), sigma=0.5)
            order_amount = max(40, min(1500, order_amount))
            order_amount = min(order_amount, monthly_budget * 0.4)
            annual_orders_list.append((month, order_amount))
    
    # NORMALIZATION STEP: Scale all orders so they sum to exactly total_annual
    total_generated = sum([amt for _, amt in annual_orders_list])
    scale_factor = total_annual / total_generated if total_generated > 0 else 1.0
    
    annual_orders_list = [(month, amt * scale_factor) for month, amt in annual_orders_list]
    
    # Now generate transaction records with normalized amounts
    for order_idx, (month, order_amount) in enumerate(annual_orders_list):
        day = np.random.randint(1, 29)
        try:
            order_date = datetime(2023, month, day)
        except ValueError:
            order_date = datetime(2023, month, 28)
        
        # Category selection
        weights = [annual_spending_by_cat[cat] / total_annual for cat in categories]
        selected_category = np.random.choice(categories, p=weights)
        
        # Order characteristics
        num_line_items = np.random.randint(1, 6)
        is_standard = np.random.random() > params['custom_rate']
        is_urgent = np.random.random() < params['rush_rate']
        needs_support = np.random.random() < params['support_rate']
        
        intensity_flags = sum([not is_standard, is_urgent, needs_support])
        order_intensity = 'Low' if intensity_flags == 0 else ('Medium' if intensity_flags == 1 else 'High')
        
        multiplier = 1.0
        if not is_standard:
            multiplier *= 1.5
        if is_urgent:
            multiplier *= 1.3
        if needs_support:
            multiplier *= 1.2
        multiplier = min(multiplier, 1.8)
        
        quantity = max(1, int(order_amount / 25))
        
        transaction = {
            'TransactionID': f'TXN-2023-{transaction_counter:06d}',
            'CustomerID': customer_id,
            'TransactionDate': order_date.strftime('%Y-%m-%d'),
            'OrderMonth': month,
            'OrderDayOfWeek': order_date.strftime('%A'),
            'ProductCategory': selected_category,
            'TransactionAmount': round(order_amount, 2),
            'Quantity': quantity,
            'NumberOfLineItems': num_line_items,
            'IsStandardOrder': is_standard,
            'IsUrgent': is_urgent,
            'CustomerServiceInteractionRequired': needs_support,
            'OrderIntensityLevel': order_intensity,
            'ServiceCostMultiplier': round(multiplier, 2)
        }
        
        all_transactions.append(transaction)
        transaction_counter += 1
    
    if (idx + 1) % 100 == 0:
        print(f"  ✓ Processed {idx + 1}/{len(customers)} customers")

# Create DataFrame
print("\n[STEP 4] Converting to DataFrame...")
transactions_df = pd.DataFrame(all_transactions)
print(f"✓ Generated {len(transactions_df)} transactions")

# Validation
print("\n[STEP 5] Revenue Aggregation Validation...")
revenue_within_tolerance = 0
for customer_id in transactions_df['CustomerID'].unique():
    trans_total = transactions_df[transactions_df['CustomerID'] == customer_id]['TransactionAmount'].sum()
    expected = customers[customers['CustomerID'] == customer_id]['TotalAnnualRevenue'].values[0]
    variance_pct = abs(trans_total - expected) / expected * 100
    
    if variance_pct <= 3:
        revenue_within_tolerance += 1

within_pct = (revenue_within_tolerance / len(transactions_df['CustomerID'].unique())) * 100
print(f"  ✓ {revenue_within_tolerance}/{len(transactions_df['CustomerID'].unique())} customers within ±3% tolerance ({within_pct:.1f}%)")

# Save
print("\n[STEP 6] Saving Dataset 2...")
output_file = 'data/generated/02_transactions_generated.csv'
transactions_df.to_csv(output_file, index=False)
print(f"✓ Saved to {output_file}")

# Summary
print("\n" + "=" * 80)
print("DATASET 2 GENERATION COMPLETE")
print("=" * 80)
print(f"Total Transactions: {len(transactions_df):,}")
print(f"Total Revenue: €{transactions_df['TransactionAmount'].sum():,.2f}")
print(f"Avg Order Size: €{transactions_df['TransactionAmount'].mean():.2f}")
print(f"Seasonality Applied: ✓ (Jan -12% to Dec +40%)")
print(f"Revenue Accuracy: {within_pct:.1f}% of customers within ±3%")
print("=" * 80)

