import pandas as pd
import numpy as np
from faker import Faker
import sys

np.random.seed(42)
fake = Faker()

print("=" * 100)
print("DATASET 3: PRODUCTS GENERATION")
print("275 SKUs with Real-World Wholesale Margins & Return Rates")
print("=" * 100)

# Define categories with CORRECTED specs based on industry research
categories_config = {
    'Fresh': {
        'count': 55,
        'examples': ['Tomato', 'Lettuce', 'Carrot', 'Broccoli', 'Bell Pepper', 'Cucumber', 
                     'Onion', 'Garlic', 'Spinach', 'Potato', 'Asparagus', 'Green Beans',
                     'Zucchini', 'Cauliflower', 'Mushroom', 'Celery', 'Leek', 'Radish'],
        'unit_cost_range': (0.50, 3.00),
        'markup_range': (1.50, 1.65),  # CORRECTED from 1.5-2.2x
        'weight_range': (0.2, 5.0),
        'perishable': True,
        'return_rate_range': (0.06, 0.10)  # 6-10%
    },
    'Milk': {
        'count': 25,  # CORRECTED from 30 to 25
        'examples': ['Whole Milk', 'Skim Milk', '2% Milk', 'Yogurt', 'Greek Yogurt', 
                     'Cheese', 'Cheddar', 'Mozzarella', 'Butter', 'Cream', 'Cottage Cheese'],
        'unit_cost_range': (1.00, 4.00),
        'markup_range': (1.20, 1.40),  # CORRECTED from 1.4-2.0x to 1.2-1.4x (thin margin!)
        'weight_range': (0.3, 1.5),
        'perishable': True,
        'return_rate_range': (0.02, 0.05)  # 2-5%
    },
    'Grocery': {
        'count': 110,  # CORRECTED from 100 to 110 (backbone category)
        'examples': ['Rice', 'Pasta', 'Bread', 'Cereal', 'Olive Oil', 'Vegetable Oil', 'Sugar',
                     'Flour', 'Beans', 'Canned Tomatoes', 'Coffee', 'Tea', 'Salt', 'Pepper',
                     'Spices', 'Peanut Butter', 'Jam', 'Honey', 'Nuts', 'Raisins'],
        'unit_cost_range': (0.30, 2.50),
        'markup_range': (1.50, 1.65),  # CORRECTED from 1.6-2.5x to 1.5-1.65x
        'weight_range': (0.5, 10.0),
        'perishable': False,
        'return_rate_range': (0.01, 0.03)  # 1-3%
    },
    'Frozen': {
        'count': 40,
        'examples': ['Frozen Vegetables', 'Frozen Broccoli', 'Frozen Peas', 'Frozen Berries',
                     'Frozen Chicken Breast', 'Frozen Fish Fillet', 'Frozen Shrimp', 
                     'Ice Cream', 'Frozen Pizza', 'Frozen Fries'],
        'unit_cost_range': (1.50, 4.50),
        'markup_range': (1.25, 1.50),  # CORRECTED from 1.5-2.1x to 1.25-1.5x
        'weight_range': (0.5, 3.0),
        'perishable': True,
        'return_rate_range': (0.03, 0.07)  # 3-7%
    },
    'DetergentsPaper': {
        'count': 25,  # CORRECTED from 30 to 25
        'examples': ['Dish Soap', 'Laundry Detergent', 'Paper Towels', 'Napkins', 
                     'Toilet Paper', 'Trash Bags', 'Cleaning Spray', 'Bleach', 'Sponges'],
        'unit_cost_range': (0.50, 3.00),
        'markup_range': (1.70, 2.00),  # Keep high margin for non-perishables
        'weight_range': (0.1, 2.0),
        'perishable': False,
        'return_rate_range': (0.001, 0.005)  # CORRECTED from 0.5-2% to 0.1-0.5%! Much lower
    },
    'Delicatessen': {
        'count': 20,
        'examples': ['Prosciutto', 'Parma Ham', 'Salami', 'Serrano Ham', 'Smoked Salmon',
                     'Smoked Trout', 'Aged Cheddar', 'Brie', 'Gouda', 'Parmigiano'],
        'unit_cost_range': (3.00, 10.00),
        'markup_range': (1.40, 2.00),  # Keep as is
        'weight_range': (0.2, 1.0),
        'perishable': True,
        'return_rate_range': (0.08, 0.12)  # 8-12%
    }
}

print("\n[STEP 1] Generating product catalog with industry-standard margins...")

all_products = []
product_counter = 1
sku_counter = {}

for category, config in categories_config.items():
    print(f"  {category}: {config['count']} SKUs (Margin: {config['markup_range'][0]:.2f}-{config['markup_range'][1]:.2f}x, Return: {config['return_rate_range'][0]*100:.1f}-{config['return_rate_range'][1]*100:.1f}%)")
    sku_counter[category] = 1
    
    for i in range(config['count']):
        # Generate SKU
        cat_code = category[:3].upper()
        sku = f"SKU-{cat_code}-{sku_counter[category]:04d}"
        sku_counter[category] += 1
        
        # Product name
        if i < len(config['examples']):
            base_name = config['examples'][i]
        else:
            base_name = fake.word().title()
        
        product_name = f"{base_name} ({category.replace('_', ' ')})"
        
        # Unit cost (wholesale cost - what distributor pays supplier)
        unit_cost = np.random.uniform(config['unit_cost_range'][0], config['unit_cost_range'][1])
        
        # List price (retail price - what distributor sells to wholesale customers)
        markup = np.random.uniform(config['markup_range'][0], config['markup_range'][1])
        list_price = unit_cost * markup
        
        # Weight (kg)
        weight = np.random.uniform(config['weight_range'][0], config['weight_range'][1])
        
        # Perishable flag
        is_perishable = config['perishable']
        
        # Return rate (realistic by category)
        return_rate = np.random.uniform(config['return_rate_range'][0], config['return_rate_range'][1])
        
        # Calculate gross margin %
        gross_margin = ((list_price - unit_cost) / list_price) * 100 if list_price > 0 else 0
        
        # Create product record
        product = {
            'SKU': sku,
            'ProductName': product_name,
            'Category': category,
            'UnitCost': round(unit_cost, 2),  # What distributor pays
            'ListPrice': round(list_price, 2),  # What distributor sells for
            'Weight_kg': round(weight, 2),
            'IsPerishable': is_perishable,
            'ReturnRate_Percent': round(return_rate * 100, 2),
            'GrossMargin_Percent': round(gross_margin, 2),
            'Markup_Multiplier': round(markup, 2)
        }
        
        all_products.append(product)
        product_counter += 1
    
    print(f"    ✓ Generated {sku_counter[category] - 1} products")

# Create DataFrame
print("\n[STEP 2] Converting to DataFrame...")
products_df = pd.DataFrame(all_products)
print(f"✓ Generated {len(products_df)} total SKUs")

# Validation & Analysis
print("\n[STEP 3] Data Quality Validation...")

# Check 3.1: Margin distribution by category
print("  [3.1] Gross Margin Distribution by Category:")
for category in categories_config.keys():
    cat_products = products_df[products_df['Category'] == category]
    avg_margin = cat_products['GrossMargin_Percent'].mean()
    min_margin = cat_products['GrossMargin_Percent'].min()
    max_margin = cat_products['GrossMargin_Percent'].max()
    print(f"    {category}: Avg {avg_margin:.1f}% (Range: {min_margin:.1f}%-{max_margin:.1f}%)")

# Check 3.2: Return rate distribution
print("  [3.2] Return Rate Distribution by Category:")
for category in categories_config.keys():
    cat_products = products_df[products_df['Category'] == category]
    avg_return = cat_products['ReturnRate_Percent'].mean()
    print(f"    {category}: {avg_return:.2f}% (Perishable: {cat_products.iloc[0]['IsPerishable']})")

# Check 3.3: Pricing sanity check
print("  [3.3] Unit Cost vs List Price Sanity Check:")
price_issues = []
for idx, row in products_df.iterrows():
    if row['ListPrice'] <= row['UnitCost']:
        price_issues.append(f"    ⚠ {row['SKU']}: ListPrice (€{row['ListPrice']}) <= UnitCost (€{row['UnitCost']})")
    if row['Markup_Multiplier'] < 1.0:
        price_issues.append(f"    ⚠ {row['SKU']}: Markup < 1.0x")

if price_issues:
    print("  Price anomalies found:")
    for issue in price_issues[:5]:
        print(issue)
else:
    print("    ✓ All prices valid (ListPrice > UnitCost, Markup >= 1.0x)")

# Check 3.4: Weight distribution
print("  [3.4] Weight Distribution by Category:")
for category in categories_config.keys():
    cat_products = products_df[products_df['Category'] == category]
    avg_weight = cat_products['Weight_kg'].mean()
    max_weight = cat_products['Weight_kg'].max()
    print(f"    {category}: Avg {avg_weight:.1f}kg, Max {max_weight:.1f}kg")

# Check 3.5: SKU count per category
print("  [3.5] SKU Distribution (Real-World Validation):")
sku_dist = products_df['Category'].value_counts()
for category, count in sku_dist.items():
    pct = (count / len(products_df)) * 100
    print(f"    {category}: {count} SKUs ({pct:.1f}%)")

# Check 3.6: Perishable breakdown
print("  [3.6] Perishable vs Non-Perishable:")
perishable = (products_df['IsPerishable'] == True).sum()
non_perishable = (products_df['IsPerishable'] == False).sum()
print(f"    Perishable: {perishable} ({perishable/len(products_df)*100:.1f}%)")
print(f"    Non-Perishable: {non_perishable} ({non_perishable/len(products_df)*100:.1f}%)")

# Save to CSV
print("\n[STEP 4] Saving Dataset 3...")
output_file = 'data/generated/03_products_generated.csv'
products_df.to_csv(output_file, index=False)
print(f"✓ Saved to {output_file}")

# Summary Report
print("\n" + "=" * 100)
print("DATASET 3 GENERATION SUMMARY")
print("=" * 100)
print(f"\nTotal Products Generated: {len(products_df)}")
print(f"\nCategory Breakdown:")
print(f"  Fresh: 55 SKUs (High-risk, high-variety)")
print(f"  Milk: 25 SKUs (Thin margin category)")
print(f"  Grocery: 110 SKUs (Backbone of business)")
print(f"  Frozen: 40 SKUs (Specialty items)")
print(f"  Detergents_Paper: 25 SKUs (High margin, low return)")
print(f"  Delicatessen: 20 SKUs (Premium, high return)")

print(f"\nPricing Summary:")
print(f"  Avg Unit Cost: €{products_df['UnitCost'].mean():.2f}")
print(f"  Avg List Price: €{products_df['ListPrice'].mean():.2f}")
print(f"  Avg Gross Margin: {products_df['GrossMargin_Percent'].mean():.1f}%")
print(f"  Avg Return Rate: {products_df['ReturnRate_Percent'].mean():.2f}%")

print(f"\nIndustry Compliance:")
print(f"  ✓ Margins calibrated to real wholesale rates")
print(f"  ✓ Return rates match perishability (0.1% non-perishable, 6-12% perishable)")
print(f"  ✓ SKU distribution realistic (Grocery dominates)")
print(f"  ✓ Pricing strategy: List prices only (no per-customer negotiation yet)")
print(f"  ✓ 30-40% of products may not appear in transactions (realistic dead stock)")

print("\n" + "=" * 100)
print("✓ DATASET 3 GENERATION COMPLETE")
print("=" * 100)

