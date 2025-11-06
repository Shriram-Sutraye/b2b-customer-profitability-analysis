import pandas as pd
import numpy as np
import sys

np.random.seed(42)

print("=" * 100)
print("DATASET 5: OUTBOUND SHIPPING COSTS (CUSTOM ORDERS ONLY)")
print("Only applies to orders where IsStandardOrder = FALSE")
print("=" * 100)

# Load datasets
print("\n[STEP 1] Loading dependent datasets...")
try:
    transactions = pd.read_csv('data/generated/02_transactions_generated.csv')
    products = pd.read_csv('data/generated/03_products_generated.csv')
    print(f"✓ Loaded {len(transactions)} transactions")
    print(f"✓ Loaded {len(products)} products")
except FileNotFoundError as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

# Shipping cost parameters
print("\n[STEP 2] Applying shipping cost logic...")

# Base shipping cost (flat for custom orders)
base_shipping = 20.00

# Weight-based surcharge (€/kg)
weight_surcharge_per_kg = 0.75

# Cold chain premiums by category
cold_chain_premium = {
    'Fresh': 20.00,           # Most stringent temperature control
    'Milk': 15.00,            # Moderate temperature control
    'Delicatessen': 18.00,    # Premium perishable
    'Frozen': 0.00,           # Already in cold chain, covered by base
    'Grocery': 0.00,          # No special handling
    'DetergentsPaper': 0.00   # Non-perishable
}

# Urgency premium (added if IsUrgent = TRUE)
urgency_premium = 20.00

print(f"✓ Base shipping: €{base_shipping:.2f}")
print(f"✓ Weight surcharge: €{weight_surcharge_per_kg}/kg")
print(f"✓ Cold chain premiums: Fresh €{cold_chain_premium['Fresh']}, Milk €{cold_chain_premium['Milk']}, Deli €{cold_chain_premium['Delicatessen']}")
print(f"✓ Urgency premium: €{urgency_premium:.2f}")

# Generate shipping costs
print("\n[STEP 3] Calculating shipping costs...")

shipping_costs = []
orders_requiring_shipping = 0
standard_orders = 0

for idx, trans in transactions.iterrows():
    transaction_id = trans['TransactionID']
    customer_id = trans['CustomerID']
    category = trans['ProductCategory']
    quantity = trans['Quantity']
    transaction_amount = trans['TransactionAmount']
    is_standard = trans.get('IsStandardOrder', True)
    is_urgent = trans.get('IsUrgent', False)
    
    # Find product average weight
    category_products = products[products['Category'] == category]
    avg_weight = category_products['Weight_kg'].mean() if len(category_products) > 0 else 1.0
    order_weight = avg_weight * quantity
    
    # ========== SHIPPING COST LOGIC ==========
    
    if is_standard:
        # Standard orders: Customer arranges their own shipping
        shipping_cost = 0.00
        standard_orders += 1
    else:
        # Custom orders: We handle shipping
        orders_requiring_shipping += 1
        
        # Base shipping cost
        cost = base_shipping
        
        # Add weight surcharge
        weight_cost = order_weight * weight_surcharge_per_kg
        cost += weight_cost
        
        # Add cold chain premium (if applicable)
        category_premium = cold_chain_premium.get(category, 0.00)
        cost += category_premium
        
        # Add urgency premium (if applicable)
        if is_urgent:
            cost += urgency_premium
        
        shipping_cost = cost
    
    # Create record
    shipping_record = {
        'TransactionID': transaction_id,
        'CustomerID': customer_id,
        'ProductCategory': category,
        'Quantity': quantity,
        'OrderWeight_kg': round(order_weight, 2),
        'TransactionAmount_EUR': round(transaction_amount, 2),
        'IsStandardOrder': is_standard,
        'IsUrgent': is_urgent,
        'BaseShippingCost_EUR': round(base_shipping, 2) if not is_standard else 0.00,
        'WeightSurchargeCost_EUR': round(weight_cost, 2) if not is_standard else 0.00,
        'ColdChainPremium_EUR': round(category_premium, 2) if not is_standard else 0.00,
        'UrgencyPremium_EUR': round(urgency_premium, 2) if (not is_standard and is_urgent) else 0.00,
        'TotalShippingCost_EUR': round(shipping_cost, 2),
        'ShippingCostPerUnit_EUR': round(shipping_cost / max(quantity, 1), 2) if shipping_cost > 0 else 0.00
    }
    
    shipping_costs.append(shipping_record)
    
    if (idx + 1) % 2000 == 0:
        print(f"  ✓ Processed {idx + 1}/{len(transactions)} transactions")

# Create DataFrame
print("\n[STEP 4] Converting to DataFrame...")
shipping_df = pd.DataFrame(shipping_costs)
print(f"✓ Generated {len(shipping_df)} shipping cost records")

# Validation
print("\n[STEP 5] Data Quality Validation...")

print("  [5.1] Order Distribution:")
print(f"    Standard orders (customer shipping): {standard_orders:,} ({standard_orders/len(shipping_df)*100:.1f}%)")
print(f"    Custom orders (we ship): {orders_requiring_shipping:,} ({orders_requiring_shipping/len(shipping_df)*100:.1f}%)")

# Only analyze custom orders
custom_orders = shipping_df[shipping_df['IsStandardOrder'] == False]
standard_only = shipping_df[shipping_df['IsStandardOrder'] == True]

print(f"\n  [5.2] Shipping Costs (Custom Orders Only):")
if len(custom_orders) > 0:
    print(f"    Min: €{custom_orders['TotalShippingCost_EUR'].min():.2f}")
    print(f"    Avg: €{custom_orders['TotalShippingCost_EUR'].mean():.2f}")
    print(f"    Max: €{custom_orders['TotalShippingCost_EUR'].max():.2f}")
    print(f"    Total: €{custom_orders['TotalShippingCost_EUR'].sum():,.2f}")
else:
    print(f"    No custom orders found")

print(f"\n  [5.3] Shipping Cost Breakdown (Custom Orders Only):")
if len(custom_orders) > 0:
    total_base = custom_orders['BaseShippingCost_EUR'].sum()
    total_weight = custom_orders['WeightSurchargeCost_EUR'].sum()
    total_cold = custom_orders['ColdChainPremium_EUR'].sum()
    total_urgency = custom_orders['UrgencyPremium_EUR'].sum()
    total_shipping = custom_orders['TotalShippingCost_EUR'].sum()
    
    print(f"    Base shipping: €{total_base:,.2f} ({total_base/total_shipping*100:.1f}%)")
    print(f"    Weight surcharge: €{total_weight:,.2f} ({total_weight/total_shipping*100:.1f}%)")
    print(f"    Cold chain premium: €{total_cold:,.2f} ({total_cold/total_shipping*100:.1f}%)")
    print(f"    Urgency premium: €{total_urgency:,.2f} ({total_urgency/total_shipping*100:.1f}%)")

print(f"\n  [5.4] Impact by Order Type:")
urgent_orders = custom_orders[custom_orders['IsUrgent'] == True]
non_urgent_orders = custom_orders[custom_orders['IsUrgent'] == False]

if len(urgent_orders) > 0:
    print(f"    Urgent custom orders: {len(urgent_orders):,} avg €{urgent_orders['TotalShippingCost_EUR'].mean():.2f}")
if len(non_urgent_orders) > 0:
    print(f"    Standard custom orders: {len(non_urgent_orders):,} avg €{non_urgent_orders['TotalShippingCost_EUR'].mean():.2f}")

print(f"\n  [5.5] Impact by Category (Custom Orders):")
for category in shipping_df['ProductCategory'].unique():
    cat_data = custom_orders[custom_orders['ProductCategory'] == category]
    if len(cat_data) > 0:
        avg_cost = cat_data['TotalShippingCost_EUR'].mean()
        count = len(cat_data)
        print(f"    {category}: {count:,} orders, avg €{avg_cost:.2f}")

# Save to CSV
print("\n[STEP 6] Saving Dataset 5...")
output_file = 'data/generated/05_shipping_costs_generated.csv'
shipping_df.to_csv(output_file, index=False)
print(f"✓ Saved to {output_file}")

# Summary
print("\n" + "=" * 100)
print("DATASET 5 GENERATION SUMMARY")
print("=" * 100)

print(f"\nShipping Costs Generated:")
print(f"  Total Transactions: {len(shipping_df):,}")
print(f"  Standard Orders (No cost): {standard_orders:,} (€0)")
print(f"  Custom Orders (With cost): {orders_requiring_shipping:,}")

if orders_requiring_shipping > 0:
    print(f"  Total Shipping Costs: €{custom_orders['TotalShippingCost_EUR'].sum():,.2f}")
    print(f"  Average per Custom Order: €{custom_orders['TotalShippingCost_EUR'].mean():.2f}")
    print(f"  Average per Unit (custom): €{custom_orders['ShippingCostPerUnit_EUR'].mean():.2f}")

print(f"\nShipping Cost Composition:")
print(f"  Base rate: €{base_shipping:.2f}")
print(f"  Weight: €{weight_surcharge_per_kg}/kg")
print(f"  Cold chain: €0-€20 (by category)")
print(f"  Urgency: €0-€20 (if rush)")

print(f"\nCost Range (Custom Orders):")
if len(custom_orders) > 0:
    min_cost = custom_orders['TotalShippingCost_EUR'].min()
    max_cost = custom_orders['TotalShippingCost_EUR'].max()
    print(f"  Minimum: €{min_cost:.2f} (light, standard)")
    print(f"  Maximum: €{max_cost:.2f} (heavy, urgent, cold chain)")
    print(f"  Typical: €40-€80")

print(f"\nKey Rules:")
print(f"  ✓ IsStandardOrder = TRUE → Customer pays (€0 to us)")
print(f"  ✓ IsStandardOrder = FALSE → We pay + cost to custom")
print(f"  ✓ IsUrgent = TRUE → Add €20 expedited premium")
print(f"  ✓ Perishable (Fresh/Milk/Deli) → Add cold chain premium")

print("\n" + "=" * 100)
print("✓ DATASET 5 GENERATION COMPLETE")
print("=" * 100)

