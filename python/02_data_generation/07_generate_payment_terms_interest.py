import pandas as pd
import numpy as np
import sys

print("=" * 100)
print("DATASET 7: PAYMENT TERMS & DSO INTEREST COST")
print("Calculate working capital financing cost based on payment terms")
print("=" * 100)

# Load datasets
print("\n[STEP 1] Loading dependent datasets...")
try:
    transactions = pd.read_csv('data/generated/02_transactions_generated.csv')
    print(f"✓ Loaded {len(transactions)} transactions")
except FileNotFoundError as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

# Payment terms to DSO mapping
print("\n[STEP 2] Applying payment terms parameters...")

payment_terms_map = {
    'Net-30': 30,      # 30 days to collect
    'Net-60': 60,      # 60 days to collect
    'Net-90': 90       # 90 days to collect
}

# Cost of capital (financing rate)
annual_interest_rate = 0.05  # 5% per year

print(f"✓ Payment terms DSO mapping: Net-30=30d, Net-60=60d, Net-90=90d")
print(f"✓ Annual interest rate: {annual_interest_rate*100:.1f}%")

# Generate payment terms interest data
print("\n[STEP 3] Calculating DSO interest costs...")

payment_data = []

for idx, trans in transactions.iterrows():
    transaction_id = trans['TransactionID']
    customer_id = trans['CustomerID']
    transaction_amount = trans['TransactionAmount']
    
    # Get payment terms from transaction
    payment_terms = trans.get('PaymentTerms', 'Net-30')
    
    # Map to DSO (days)
    dso_days = payment_terms_map.get(payment_terms, 30)
    
    # Calculate interest cost
    # Formula: (Order Value × DSO × Annual Interest Rate) / 365 days
    annual_interest = transaction_amount * annual_interest_rate
    daily_interest = annual_interest / 365
    dso_interest_cost = daily_interest * dso_days
    
    # Create record
    payment_record = {
        'TransactionID': transaction_id,
        'CustomerID': customer_id,
        'TransactionAmount_EUR': round(transaction_amount, 2),
        'PaymentTerms': payment_terms,
        'DSO_Days': dso_days,
        'AnnualInterestRate': annual_interest_rate,
        'DailyInterestCost_EUR': round(daily_interest, 4),
        'DSO_InterestCost_EUR': round(dso_interest_cost, 2)
    }
    
    payment_data.append(payment_record)
    
    if (idx + 1) % 2000 == 0:
        print(f"  ✓ Processed {idx + 1}/{len(transactions)} transactions")

# Create DataFrame
print("\n[STEP 4] Converting to DataFrame...")
payment_df = pd.DataFrame(payment_data)
print(f"✓ Generated {len(payment_df)} payment terms interest records")

# Validation
print("\n[STEP 5] Data Quality Validation...")

print(f"\n  [5.1] Payment Terms Distribution:")
terms_dist = payment_df['PaymentTerms'].value_counts()
for term, count in terms_dist.items():
    pct = count / len(payment_df) * 100
    print(f"    {term}: {count:,} ({pct:.1f}%)")

print(f"\n  [5.2] DSO Interest Cost Analysis:")
print(f"    Minimum: €{payment_df['DSO_InterestCost_EUR'].min():.2f}")
print(f"    Average: €{payment_df['DSO_InterestCost_EUR'].mean():.2f}")
print(f"    Maximum: €{payment_df['DSO_InterestCost_EUR'].max():.2f}")
print(f"    Total: €{payment_df['DSO_InterestCost_EUR'].sum():,.2f}")

print(f"\n  [5.3] Interest Cost by Payment Term:")
for term in ['Net-30', 'Net-60', 'Net-90']:
    term_data = payment_df[payment_df['PaymentTerms'] == term]
    if len(term_data) > 0:
        avg_cost = term_data['DSO_InterestCost_EUR'].mean()
        print(f"    {term}: €{avg_cost:.2f} average")

print(f"\n  [5.4] Interest Cost as % of Revenue:")
revenue_pct = (payment_df['DSO_InterestCost_EUR'].sum() / payment_df['TransactionAmount_EUR'].sum()) * 100
print(f"    Total interest: {revenue_pct:.2f}% of revenue")

# Save to CSV
print("\n[STEP 6] Saving Dataset 7...")
output_file = 'data/generated/07_payment_terms_interest_generated.csv'
payment_df.to_csv(output_file, index=False)
print(f"✓ Saved to {output_file}")

# Summary
print("\n" + "=" * 100)
print("DATASET 7 GENERATION SUMMARY")
print("=" * 100)

print(f"\nPayment Terms & Interest Cost:")
print(f"  Total Transactions: {len(payment_df):,}")
print(f"  Total Interest Cost: €{payment_df['DSO_InterestCost_EUR'].sum():,.2f}")
print(f"  Average per Order: €{payment_df['DSO_InterestCost_EUR'].mean():.2f}")

print(f"\nPayment Terms Breakdown:")
for term in ['Net-30', 'Net-60', 'Net-90']:
    term_data = payment_df[payment_df['PaymentTerms'] == term]
    if len(term_data) > 0:
        count = len(term_data)
        total_cost = term_data['DSO_InterestCost_EUR'].sum()
        print(f"  {term}: {count:,} orders, €{total_cost:,.2f} total interest")

print(f"\nKey Insights:")
print(f"  DSO Interest adds €{payment_df['DSO_InterestCost_EUR'].mean():.2f} per order")
print(f"  This is {revenue_pct:.2f}% of average revenue (€{payment_df['TransactionAmount_EUR'].mean():.2f})")
print(f"  Net-30 customers: Lowest interest cost")
print(f"  Net-90 customers: 3x higher interest cost than Net-30")

print("\n" + "=" * 100)
print("✓ DATASET 7 GENERATION COMPLETE")
print("=" * 100)

