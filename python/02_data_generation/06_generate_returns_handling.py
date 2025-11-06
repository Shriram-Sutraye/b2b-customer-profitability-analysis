import pandas as pd
import numpy as np
import sys

np.random.seed(42)

print("=" * 100)
print("DATASET 6: RETURNS HANDLING & REVERSE LOGISTICS")
print("Industry-standard return rates, reverse shipping, disposal costs")
print("=" * 100)

# Load datasets
print("\n[STEP 1] Loading dependent datasets...")
try:
    transactions = pd.read_csv('data/generated/02_transactions_generated.csv')
    products = pd.read_csv('data/generated/03_products_generated.csv')
    warehouse = pd.read_csv('data/generated/04_warehouse_costs_generated.csv')
    print(f"✓ Loaded {len(transactions)} transactions")
    print(f"✓ Loaded {len(products)} products")
    print(f"✓ Loaded {len(warehouse)} warehouse records")
except FileNotFoundError as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

# Industry-standard return rates by category
print("\n[STEP 2] Applying industry-standard return parameters...")

return_rates = {
    'Fresh': 0.12,              # 12% - Highest risk (spoilage, damage)
    'Milk': 0.08,               # 8% - Temperature sensitive
    'Deli': 0.15,               # 15% - Premium, high handling
    'Frozen': 0.04,             # 4% - Stable items
    'Grocery': 0.02,            # 2% - Durable
    'DetergentsPaper': 0.01     # 1% - Rarely damaged
}

# Return disposition split (industry standard)
resellable_pct = 0.60          # 60% can be restocked
discounted_pct = 0.20          # 20% sold at discount (40% loss)
scrap_pct = 0.20               # 20% scrapped (100% loss + disposal)

# Return responsibility
responsibility = {
    'OurError': 1.0,            # We pay 100%
    'ShippingDamage': 0.5,      # Split 50/50
    'CustomerComplaint': 1.0,   # We pay 100%
    'QualityIssue': 1.0         # We pay 100%
}

# Reverse logistics costs
reverse_base = 20.00            # Base return shipping €20
cold_chain_premium = 5.00       # +€5 for Fresh/Milk/Deli
handling_receiving = 2.50       # Receiving cost per return
handling_qc = 2.50              # QC cost per return
restocking_per_kg = 0.33        # Restocking labor per kg

# Disposal cost
disposal_cost_per_kg = 0.20     # €0.20 per kg for scrap

print(f"✓ Return rates: Fresh 12%, Milk 8%, Deli 15%, Frozen 4%, Grocery 2%, Detergent 1%")
print(f"✓ Disposition: Resellable 60%, Discounted 20%, Scrap 20%")
print(f"✓ Reverse shipping: €20 base + €5 cold chain")
print(f"✓ Handling labor: €2.50 receiving + €2.50 QC + €0.33/kg restocking")
print(f"✓ Disposal: €0.20/kg for scrap")

# Generate returns data
print("\n[STEP 3] Calculating return costs for each transaction...")

returns_data = []

for idx, trans in transactions.iterrows():
    transaction_id = trans['TransactionID']
    customer_id = trans['CustomerID']
    category = trans['ProductCategory']
    quantity = trans['Quantity']
    transaction_amount = trans['TransactionAmount']
    is_standard = trans.get('IsStandardOrder', True)
    is_urgent = trans.get('IsUrgent', False)
    
    # Get warehouse record for weight
    warehouse_record = warehouse[warehouse['TransactionID'] == transaction_id]
    if len(warehouse_record) == 0:
        continue
    
    order_weight = warehouse_record.iloc[0]['OrderWeight_kg']
    
    # Determine if order is returned based on industry rates
    return_rate = return_rates.get(category, 0.05)
    is_returned = np.random.random() < return_rate
    
    if not is_returned:
        # No return for this order
        return_record = {
            'TransactionID': transaction_id,
            'CustomerID': customer_id,
            'ProductCategory': category,
            'Quantity': quantity,
            'OrderWeight_kg': order_weight,
            'TransactionAmount_EUR': round(transaction_amount, 2),
            'IsStandardOrder': is_standard,
            'IsReturned': False,
            'ReturnRate': return_rate,
            'ReverseShippingCost_EUR': 0.00,
            'ReceivingCost_EUR': 0.00,
            'QCCost_EUR': 0.00,
            'RestockingCost_EUR': 0.00,
            'DisposalCost_EUR': 0.00,
            'ResellableValue_EUR': 0.00,
            'DiscountedLoss_EUR': 0.00,
            'ScrapLoss_EUR': 0.00,
            'TotalReturnExpense_EUR': 0.00
        }
    else:
        # Order is returned
        
        # 1. REVERSE TRANSPORTATION
        if is_standard:
            # Standard order: Customer arranges return
            reverse_shipping = 0.00
        else:
            # Custom order: We pay
            reverse_shipping = reverse_base
            # Add cold chain premium if perishable
            if category in ['Fresh', 'Milk', 'Delicatessen']:
                reverse_shipping += cold_chain_premium
        
        # 2. HANDLING COSTS
        receiving_cost = handling_receiving
        qc_cost = handling_qc
        restocking_cost = (order_weight / 2) * restocking_per_kg  # Half weight is restocked
        
        # 3. PRODUCT DISPOSITION
        returned_value = transaction_amount
        
        # 60% resellable (no loss)
        resellable_value = returned_value * resellable_pct
        
        # 20% discounted at 40% loss
        discounted_value = returned_value * discounted_pct
        discounted_loss = discounted_value * 0.40
        
        # 20% scrap (100% loss)
        scrap_value = returned_value * scrap_pct
        scrap_loss = scrap_value
        
        total_value_loss = discounted_loss + scrap_loss
        
        # 4. DISPOSAL COSTS
        scrap_weight = order_weight * scrap_pct
        disposal_cost = scrap_weight * disposal_cost_per_kg
        
        # 5. RETURN REASON (assign randomly)
        reasons = list(responsibility.keys())
        return_reason = np.random.choice(reasons)
        responsibility_pct = responsibility[return_reason]
        
        # TOTAL RETURN EXPENSE
        base_cost = reverse_shipping + receiving_cost + qc_cost + restocking_cost + disposal_cost
        total_return_cost = (base_cost * responsibility_pct) + total_value_loss
        
        return_record = {
            'TransactionID': transaction_id,
            'CustomerID': customer_id,
            'ProductCategory': category,
            'Quantity': quantity,
            'OrderWeight_kg': round(order_weight, 2),
            'TransactionAmount_EUR': round(transaction_amount, 2),
            'IsStandardOrder': is_standard,
            'IsReturned': True,
            'ReturnRate': return_rate,
            'ReturnReason': return_reason,
            'ResponsibilityPercentage': responsibility_pct,
            'ReverseShippingCost_EUR': round(reverse_shipping, 2),
            'ReceivingCost_EUR': round(receiving_cost, 2),
            'QCCost_EUR': round(qc_cost, 2),
            'RestockingCost_EUR': round(restocking_cost, 2),
            'DisposalCost_EUR': round(disposal_cost, 2),
            'ResellableValue_EUR': round(resellable_value, 2),
            'DiscountedLoss_EUR': round(discounted_loss, 2),
            'ScrapLoss_EUR': round(scrap_loss, 2),
            'TotalReturnExpense_EUR': round(total_return_cost, 2)
        }
    
    returns_data.append(return_record)
    
    if (idx + 1) % 2000 == 0:
        print(f"  ✓ Processed {idx + 1}/{len(transactions)} transactions")

# Create DataFrame
print("\n[STEP 4] Converting to DataFrame...")
returns_df = pd.DataFrame(returns_data)
print(f"✓ Generated {len(returns_df)} return cost records")

# Validation
print("\n[STEP 5] Data Quality Validation...")

returned_orders = returns_df[returns_df['IsReturned'] == True]
returned_count = len(returned_orders)
returned_pct = (returned_count / len(returns_df)) * 100

print(f"\n  [5.1] Return Distribution:")
print(f"    Total orders: {len(returns_df):,}")
print(f"    Orders with returns: {returned_count:,} ({returned_pct:.1f}%)")
print(f"    No returns: {len(returns_df) - returned_count:,}")

if len(returned_orders) > 0:
    print(f"\n  [5.2] Return Costs Analysis:")
    print(f"    Total return expenses: €{returned_orders['TotalReturnExpense_EUR'].sum():,.2f}")
    print(f"    Average per returned order: €{returned_orders['TotalReturnExpense_EUR'].mean():.2f}")
    print(f"    Min return cost: €{returned_orders['TotalReturnExpense_EUR'].min():.2f}")
    print(f"    Max return cost: €{returned_orders['TotalReturnExpense_EUR'].max():.2f}")
    
    print(f"\n  [5.3] Cost Breakdown (% of Total Return Expense):")
    total_expense = returned_orders['TotalReturnExpense_EUR'].sum()
    if total_expense > 0:
        print(f"    Reverse shipping: {returned_orders['ReverseShippingCost_EUR'].sum()/total_expense*100:.1f}%")
        print(f"    Receiving: {returned_orders['ReceivingCost_EUR'].sum()/total_expense*100:.1f}%")
        print(f"    QC: {returned_orders['QCCost_EUR'].sum()/total_expense*100:.1f}%")
        print(f"    Restocking: {returned_orders['RestockingCost_EUR'].sum()/total_expense*100:.1f}%")
        print(f"    Disposal: {returned_orders['DisposalCost_EUR'].sum()/total_expense*100:.1f}%")
        print(f"    Value loss (discount+scrap): {(returned_orders['DiscountedLoss_EUR'].sum() + returned_orders['ScrapLoss_EUR'].sum())/total_expense*100:.1f}%")
    
    print(f"\n  [5.4] Returns by Category:")
    for category in returns_df['ProductCategory'].unique():
        cat_returns = returned_orders[returned_orders['ProductCategory'] == category]
        cat_all = returns_df[returns_df['ProductCategory'] == category]
        if len(cat_all) > 0:
            rate = len(cat_returns) / len(cat_all) * 100
            avg_cost = cat_returns['TotalReturnExpense_EUR'].mean() if len(cat_returns) > 0 else 0
            print(f"    {category}: {rate:.1f}% return rate, avg €{avg_cost:.2f} per return")
    
    print(f"\n  [5.5] Returns by Order Type:")
    custom_returns = returned_orders[returned_orders['IsStandardOrder'] == False]
    standard_returns = returned_orders[returned_orders['IsStandardOrder'] == True]
    if len(custom_returns) > 0:
        print(f"    Custom orders: {len(custom_returns)} returns, avg €{custom_returns['TotalReturnExpense_EUR'].mean():.2f}")
    if len(standard_returns) > 0:
        print(f"    Standard orders: {len(standard_returns)} returns, avg €{standard_returns['TotalReturnExpense_EUR'].mean():.2f}")

# Save to CSV
print("\n[STEP 6] Saving Dataset 6...")
output_file = 'data/generated/06_returns_handling_generated.csv'
returns_df.to_csv(output_file, index=False)
print(f"✓ Saved to {output_file}")

# Summary
print("\n" + "=" * 100)
print("DATASET 6 GENERATION SUMMARY")
print("=" * 100)

print(f"\nReturns Handling Costs:")
print(f"  Total Transactions: {len(returns_df):,}")
print(f"  Transactions with Returns: {returned_count:,} ({returned_pct:.1f}%)")

if len(returned_orders) > 0:
    print(f"  Total Return Costs: €{returned_orders['TotalReturnExpense_EUR'].sum():,.2f}")
    print(f"  Average per Returned Order: €{returned_orders['TotalReturnExpense_EUR'].mean():.2f}")
    
    print(f"\nReturn Cost Distribution:")
    print(f"  Reverse shipping: €{returned_orders['ReverseShippingCost_EUR'].sum():,.2f}")
    print(f"  Handling (receiving+QC): €{(returned_orders['ReceivingCost_EUR'].sum() + returned_orders['QCCost_EUR'].sum()):,.2f}")
    print(f"  Restocking: €{returned_orders['RestockingCost_EUR'].sum():,.2f}")
    print(f"  Disposal: €{returned_orders['DisposalCost_EUR'].sum():,.2f}")
    print(f"  Value loss: €{(returned_orders['DiscountedLoss_EUR'].sum() + returned_orders['ScrapLoss_EUR'].sum()):,.2f}")

print(f"\nIndustry Benchmarks Applied:")
print(f"  Return rates: Fresh 12%, Milk 8%, Deli 15%, Frozen 4%, Grocery 2%, Detergent 1%")
print(f"  Disposition: Resellable 60%, Discounted 20%, Scrap 20%")
print(f"  Reverse shipping: €20 base + €5 cold chain for custom")
print(f"  Handling labor: €5 base + €0.33/kg restocking")

print("\n" + "=" * 100)
print("✓ DATASET 6 GENERATION COMPLETE")
print("=" * 100)

