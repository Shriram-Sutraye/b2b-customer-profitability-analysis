import pandas as pd
import numpy as np
import sys

np.random.seed(42)

print("=" * 100)
print("DATASET 4: WAREHOUSE OPERATIONS COSTS (FULLY CORRECTED - ALL 4 ISSUES FIXED)")
print("Issue 1: Labor rates increased | Issue 2: Inbound flat rate | Issue 3: Custom flag | Issue 4: Cold chain capped")
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

# FULLY CORRECTED B2B parameters
print("\n[STEP 2] Applying FULLY CORRECTED parameters...")

# FIX 1: LABOR RATES INCREASED (€6.00-7.50 per item instead of €4-5)
labor_pick_pack_per_item = {
    'Fresh': 7.50,        # INCREASED from 5.50
    'Milk': 6.50,         # INCREASED from 4.80
    'Grocery': 6.00,      # INCREASED from 4.50
    'Frozen': 6.50,       # INCREASED from 4.80
    'DetergentsPaper': 5.50,  # INCREASED from 4.20
    'Delicatessen': 7.00  # INCREASED from 5.00
}

# Receiving labor (per order) - INCREASED
receiving_cost_per_order = 5.00  # INCREASED from 3.50

# Put-away labor (per unit) - INCREASED
putaway_cost_per_unit = 0.65  # INCREASED from 0.45

# Storage cost (per kg per day)
storage_cost_per_kg_day = {
    'Fresh': 0.30,
    'Milk': 0.35,
    'Grocery': 0.10,
    'Frozen': 0.40,
    'DetergentsPaper': 0.08,
    'Delicatessen': 0.32
}

# Storage duration (days)
storage_duration_days = {
    'Low': 1.0,
    'Medium': 1.5,
    'High': 2.0
}

# Indirect labor (supervision)
indirect_labor_pct = 0.15

# FIX 2: INBOUND TRANSPORT - FLAT RATE NOT % (€10 per order instead of 3%)
inbound_transport_flat = 10.00  # Flat €10 per order (not % of value)

# Shrinkage/Spoilage
shrinkage_rate = {
    'Fresh': 0.05,
    'Milk': 0.03,
    'Grocery': 0.01,
    'Frozen': 0.02,
    'DetergentsPaper': 0.005,
    'Delicatessen': 0.08
}

# FIX 3: RETURNS NOW USES IsCustomOrder FLAG (if it exists)
returns_rate_standard = {
    'Fresh': 0.03,
    'Milk': 0.02,
    'Grocery': 0.01,
    'Frozen': 0.02,
    'DetergentsPaper': 0.005,
    'Delicatessen': 0.05
}

returns_rate_custom = {
    'Fresh': 0.08,
    'Milk': 0.05,
    'Grocery': 0.03,
    'Frozen': 0.05,
    'DetergentsPaper': 0.01,
    'Delicatessen': 0.10
}

# Equipment/Technology
equipment_tech_pct = 0.05

# FIX 4: COLD CHAIN CAPPED AT 1.5x (not 2.0x)
cold_chain_multiplier_cap = 1.5  # CAPPED from 2.04x

perishable_categories = ['Fresh', 'Milk', 'Delicatessen']

print(f"✓ FIX 1: Labor rates INCREASED (€5.50-7.50/item)")
print(f"✓ FIX 2: Receiving €5.00/order, Put-away €0.65/unit")
print(f"✓ FIX 3: Inbound transport FLAT €10/order (not %)")
print(f"✓ FIX 4: Returns vary by custom/standard (uses flag)")
print(f"✓ FIX 5: Cold chain multiplier CAPPED at 1.5x")

# Generate warehouse costs
print("\n[STEP 3] Calculating FULLY CORRECTED warehouse costs...")

warehouse_costs = []

for idx, trans in transactions.iterrows():
    transaction_id = trans['TransactionID']
    customer_id = trans['CustomerID']
    category = trans['ProductCategory']
    num_line_items = trans['NumberOfLineItems']
    quantity = trans['Quantity']
    transaction_amount = trans['TransactionAmount']
    order_intensity = trans['OrderIntensityLevel']
    service_multiplier = trans['ServiceCostMultiplier']
    
    # FIX 3: Try to get IsCustomOrder flag, default to False
    is_custom = trans.get('IsCustomOrder', False)
    
    # Find product average weight
    category_products = products[products['Category'] == category]
    avg_weight = category_products['Weight_kg'].mean() if len(category_products) > 0 else 1.0
    order_weight = avg_weight * quantity
    
    # ========== 1. PICKING & PACKING LABOR (FIX 1: INCREASED) ==========
    labor_rate_per_item = labor_pick_pack_per_item.get(category, 6.50)
    pick_pack_cost = labor_rate_per_item * num_line_items
    
    # ========== 2. RECEIVING LABOR (FIX 1: INCREASED) ==========
    receiving_cost = receiving_cost_per_order
    
    # ========== 3. PUT-AWAY LABOR (FIX 1: INCREASED) ==========
    putaway_cost = putaway_cost_per_unit * quantity
    
    # ========== 4. STORAGE/OCCUPANCY COST ==========
    storage_duration = storage_duration_days.get(order_intensity, 1.0)
    storage_cost_per_kg_day_cat = storage_cost_per_kg_day.get(category, 0.15)
    storage_cost = order_weight * storage_cost_per_kg_day_cat * storage_duration
    
    # ========== 5. INDIRECT LABOR (SUPERVISION) ==========
    direct_labor_subtotal = pick_pack_cost + receiving_cost + putaway_cost
    indirect_labor_cost = direct_labor_subtotal * indirect_labor_pct
    
    # ========== 6. FIX 2: INBOUND TRANSPORT (FLAT €10, NOT %) ==========
    inbound_transport_cost = inbound_transport_flat
    
    # ========== 7. SHRINKAGE/SPOILAGE/DAMAGE ==========
    shrinkage_pct = shrinkage_rate.get(category, 0.02)
    shrinkage_cost = transaction_amount * shrinkage_pct
    
    # ========== 8. FIX 3: RETURNS (VARIES BY CUSTOM/STANDARD) ==========
    if is_custom:
        returns_pct = returns_rate_custom.get(category, 0.05)
    else:
        returns_pct = returns_rate_standard.get(category, 0.02)
    returns_cost = transaction_amount * returns_pct
    
    # ========== 9. EQUIPMENT/TECHNOLOGY ALLOCATION ==========
    subtotal_before_equipment = (pick_pack_cost + receiving_cost + putaway_cost + 
                                 storage_cost + indirect_labor_cost)
    equipment_tech_cost = subtotal_before_equipment * equipment_tech_pct
    
    # ========== SUBTOTAL ==========
    total_base_cost = (pick_pack_cost + receiving_cost + putaway_cost + 
                       storage_cost + indirect_labor_cost + inbound_transport_cost + 
                       shrinkage_cost + returns_cost + equipment_tech_cost)
    
    # ========== FIX 4: COLD CHAIN MULTIPLIER (CAPPED at 1.5x) ==========
    cold_chain_multiplier = cold_chain_multiplier_cap if category in perishable_categories else 1.0
    
    # ========== APPLY SERVICE COST MULTIPLIER ==========
    total_ops_cost = total_base_cost * service_multiplier * cold_chain_multiplier
    
    # Create record
    warehouse_cost_record = {
        'TransactionID': transaction_id,
        'CustomerID': customer_id,
        'ProductCategory': category,
        'OrderIntensity': order_intensity,
        'IsCustomOrder': is_custom,
        'Quantity': quantity,
        'NumberOfLineItems': num_line_items,
        'OrderWeight_kg': round(order_weight, 2),
        'TransactionAmount_EUR': round(transaction_amount, 2),
        'PickPackCost_EUR': round(pick_pack_cost, 2),
        'ReceivingCost_EUR': round(receiving_cost, 2),
        'PutawayCost_EUR': round(putaway_cost, 2),
        'StorageCost_EUR': round(storage_cost, 2),
        'IndirectLaborCost_EUR': round(indirect_labor_cost, 2),
        'InboundTransportCost_EUR': round(inbound_transport_cost, 2),
        'ShrinkageCost_EUR': round(shrinkage_cost, 2),
        'ReturnsCost_EUR': round(returns_cost, 2),
        'EquipmentTechCost_EUR': round(equipment_tech_cost, 2),
        'ColdChainMultiplier': cold_chain_multiplier,
        'ServiceCostMultiplier': service_multiplier,
        'TotalWarehouseOperationsCost_EUR': round(total_ops_cost, 2),
        'CostPerUnit_EUR': round(total_ops_cost / max(quantity, 1), 2)
    }
    
    warehouse_costs.append(warehouse_cost_record)
    
    if (idx + 1) % 2000 == 0:
        print(f"  ✓ Processed {idx + 1}/{len(transactions)} transactions")

# Create DataFrame
print("\n[STEP 4] Converting to DataFrame...")
warehouse_df = pd.DataFrame(warehouse_costs)
print(f"✓ Generated {len(warehouse_df)} warehouse cost records")

# Validation
print("\n[STEP 5] Data Quality Validation...")

total_pick_pack = warehouse_df['PickPackCost_EUR'].sum()
total_receiving = warehouse_df['ReceivingCost_EUR'].sum()
total_putaway = warehouse_df['PutawayCost_EUR'].sum()
total_storage = warehouse_df['StorageCost_EUR'].sum()
total_indirect = warehouse_df['IndirectLaborCost_EUR'].sum()
total_inbound = warehouse_df['InboundTransportCost_EUR'].sum()
total_shrinkage = warehouse_df['ShrinkageCost_EUR'].sum()
total_returns = warehouse_df['ReturnsCost_EUR'].sum()
total_equipment = warehouse_df['EquipmentTechCost_EUR'].sum()
total_ops = warehouse_df['TotalWarehouseOperationsCost_EUR'].sum()

total_labor = total_pick_pack + total_receiving + total_putaway + total_indirect

print("  [5.1] Cost Distribution:")
print(f"    Min: €{warehouse_df['TotalWarehouseOperationsCost_EUR'].min():.2f}")
print(f"    Avg: €{warehouse_df['TotalWarehouseOperationsCost_EUR'].mean():.2f}")
print(f"    Max: €{warehouse_df['TotalWarehouseOperationsCost_EUR'].max():.2f}")

print("  [5.2] Complete Cost Breakdown (% of Total):")
print(f"    Direct Labor (FIX 1 INCREASED): {total_labor/total_ops*100:.1f}%")
print(f"    Storage: {total_storage/total_ops*100:.1f}%")
print(f"    Inbound Transport (FIX 2 FLAT): {total_inbound/total_ops*100:.1f}%")
print(f"    Shrinkage: {total_shrinkage/total_ops*100:.1f}%")
print(f"    Returns (FIX 3 VARIES): {total_returns/total_ops*100:.1f}%")
print(f"    Equipment: {total_equipment/total_ops*100:.1f}%")

print(f"  [5.3] Benchmarks Alignment:")
print(f"    Labor: {total_labor/total_ops*100:.1f}% (Target: 30-40%)")
print(f"    Storage: {total_storage/total_ops*100:.1f}% (Target: 10-20%)")
print(f"    Inbound: {total_inbound/total_ops*100:.1f}% (Target: 2-4%)")
print(f"    Returns: {total_returns/total_ops*100:.1f}% (Target: 5-10%)")

# Save to CSV
print("\n[STEP 6] Saving Dataset 4...")
output_file = 'data/generated/04_warehouse_costs_generated.csv'
warehouse_df.to_csv(output_file, index=False)
print(f"✓ Saved to {output_file}")

# Summary
print("\n" + "=" * 100)
print("DATASET 4 FULLY CORRECTED SUMMARY")
print("=" * 100)

print(f"\nWarehouse Operations Costs:")
print(f"  Total Transactions: {len(warehouse_df):,}")
print(f"  Total Warehouse Costs: €{total_ops:,.2f}")
print(f"  Average Cost Per Order: €{warehouse_df['TotalWarehouseOperationsCost_EUR'].mean():.2f}")

print(f"\nAll Fixes Applied:")
print(f"  ✓ FIX 1: Labor rates INCREASED (€5.50-7.50 per item)")
print(f"  ✓ FIX 2: Inbound transport FLAT €10/order (not 3%)")
print(f"  ✓ FIX 3: Returns vary by custom/standard (IsCustomOrder flag)")
print(f"  ✓ FIX 4: Cold chain multiplier CAPPED at 1.5x")
print(f"  ✓ FIX 5: NO outbound transport (Dataset 5 only)")

print("\n" + "=" * 100)
print("✓ DATASET 4 FULLY CORRECTED GENERATION COMPLETE")
print("=" * 100)

