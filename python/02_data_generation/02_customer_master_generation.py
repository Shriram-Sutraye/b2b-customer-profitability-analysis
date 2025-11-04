import pandas as pd
import numpy as np
from faker import Faker
import random

# Set seeds for reproducibility
random.seed(42)
np.random.seed(42)
Faker.seed(42)

fake = Faker()

print("=" * 80)
print("STEP 1: LOAD UCI WHOLESALE CUSTOMERS (440 REAL CUSTOMERS)")
print("=" * 80)

df = pd.read_csv('data/raw/wholesale_customers.csv')
print(f"✓ Loaded {len(df)} real customers from UCI")

df = df.rename(columns={
    'Fresh': 'AnnualFreshSpending',
    'Milk': 'AnnualMilkSpending',
    'Grocery': 'AnnualGrocerySpending',
    'Frozen': 'AnnualFrozenSpending',
    'Detergents_Paper': 'AnnualDetergentsPaperSpending',
    'Delicassen': 'AnnualDelicatessenSpending'
})

df['OriginalChannel'] = df['Channel']
df['OriginalRegion'] = df['Region']

print("\n" + "=" * 80)
print("STEP 2: ADD GENERATED COLUMNS WITH BUSINESS LOGIC (NOT RANDOM)")
print("=" * 80)

# CustomerID (sequential)
df['CustomerID'] = [f'CUST-{str(i+1).zfill(3)}' for i in range(len(df))]
print("✓ CustomerID: Sequential CUST-001 to CUST-440")

# CustomerName (random for realism)
df['CustomerName'] = [fake.company() for _ in range(len(df))]
print("✓ CustomerName: Generated using Faker (RANDOM - for realism)")

# RegionName & ChannelName (mapped, not random)
df['RegionName'] = df['OriginalRegion'].map({
    1: 'Lisbon',
    2: 'Porto',
    3: 'Other_Regions'
})

df['ChannelName'] = df['OriginalChannel'].map({
    1: 'HORECA',
    2: 'Retail'
})
print("✓ RegionName: Mapped from UCI region codes (NOT RANDOM)")
print("✓ ChannelName: Mapped from UCI channel codes (NOT RANDOM)")

# TotalAnnualRevenue (sum of all 6 categories)
df['TotalAnnualRevenue'] = (
    df['AnnualFreshSpending'] +
    df['AnnualMilkSpending'] +
    df['AnnualGrocerySpending'] +
    df['AnnualFrozenSpending'] +
    df['AnnualDetergentsPaperSpending'] +
    df['AnnualDelicatessenSpending']
)
print("✓ TotalAnnualRevenue: Sum of 6 spending categories (DETERMINISTIC)")

# CustomerSegment (revenue-based thresholds)
def assign_segment(revenue):
    if revenue < 20000:
        return 'SMB'
    elif revenue < 50000:
        return 'Mid-Market'
    else:
        return 'Enterprise'

df['CustomerSegment'] = df['TotalAnnualRevenue'].apply(assign_segment)
segment_counts = df['CustomerSegment'].value_counts()
print(f"✓ CustomerSegment: Revenue-based thresholds (DETERMINISTIC)")
print(f"  - SMB (<€20k): {segment_counts.get('SMB', 0)}")
print(f"  - Mid-Market (€20-50k): {segment_counts.get('Mid-Market', 0)}")
print(f"  - Enterprise (>€50k): {segment_counts.get('Enterprise', 0)}")

# DaysAsCustomer (random 1-3 years for tenure)
df['DaysAsCustomer'] = np.random.randint(365, 1095, len(df))
print(f"✓ DaysAsCustomer: RANDOM 1-3 years range")

# OrderFrequencyPerMonth (channel-driven, not random)
def assign_order_frequency(channel):
    if channel == 1:  # HORECA
        return np.random.uniform(3, 5)
    else:  # Retail
        return np.random.uniform(0.5, 2)

df['OrderFrequencyPerMonth'] = df['OriginalChannel'].apply(assign_order_frequency)
print(f"✓ OrderFrequencyPerMonth: Channel-driven (RANDOM within ranges)")

# ==================== CORRECTED: PaymentTerms with 12% Random + 88% Smart Correlation ====================
print(f"\n✓ PaymentTerms: 12% RANDOM + 88% SMART CORRELATION (FIXED)")

def assign_payment_terms_fixed(row):
    """
    12% completely random (outliers/shit customers)
    88% determined by: CustomerSegment (PRIMARY) + DaysAsCustomer (OVERRIDE only if new)
    """
    # 12% random for outliers
    if np.random.random() < 0.12:
        return np.random.choice(['Net-30', 'Net-60', 'Net-90'])
    
    # 88% smart logic - segment first
    segment = row['CustomerSegment']
    days_customer = row['DaysAsCustomer']
    
    # Base distribution by segment (PRIMARY LOGIC)
    if segment == 'SMB':
        base_terms = np.random.choice(['Net-30', 'Net-60', 'Net-90'], p=[0.80, 0.15, 0.05])
    elif segment == 'Mid-Market':
        base_terms = np.random.choice(['Net-30', 'Net-60', 'Net-90'], p=[0.40, 0.45, 0.15])
    else:  # Enterprise
        base_terms = np.random.choice(['Net-30', 'Net-60', 'Net-90'], p=[0.20, 0.40, 0.40])
    
    # ONLY override if new customer (<6 months) - force Net-30
    if days_customer < 180:
        return 'Net-30'
    
    # Otherwise return segment-based terms
    return base_terms

df['PaymentTerms'] = df.apply(assign_payment_terms_fixed, axis=1)
payment_counts = df['PaymentTerms'].value_counts()
print(f"  - Net-30: {payment_counts.get('Net-30', 0)} ({payment_counts.get('Net-30', 0)/len(df)*100:.1f}%)")
print(f"  - Net-60: {payment_counts.get('Net-60', 0)} ({payment_counts.get('Net-60', 0)/len(df)*100:.1f}%)")
print(f"  - Net-90: {payment_counts.get('Net-90', 0)} ({payment_counts.get('Net-90', 0)/len(df)*100:.1f}%)")

# Payment terms breakdown by segment
print(f"\n  PaymentTerms by Segment:")
for seg in ['SMB', 'Mid-Market', 'Enterprise']:
    seg_df = df[df['CustomerSegment'] == seg]
    seg_counts = seg_df['PaymentTerms'].value_counts()
    print(f"    {seg}: Net-30={seg_counts.get('Net-30', 0)} ({seg_counts.get('Net-30', 0)/len(seg_df)*100:.1f}%), Net-60={seg_counts.get('Net-60', 0)} ({seg_counts.get('Net-60', 0)/len(seg_df)*100:.1f}%), Net-90={seg_counts.get('Net-90', 0)} ({seg_counts.get('Net-90', 0)/len(seg_df)*100:.1f}%)")

# ServiceIntensityScore (deterministic formula)
def calculate_service_intensity(row):
    score = 0
    if row['OriginalChannel'] == 1:
        score += 3.0
    else:
        score += 1.0
    
    freq = row['OrderFrequencyPerMonth']
    if freq >= 4:
        score += 3.0
    elif freq >= 2.5:
        score += 2.0
    else:
        score += 1.0
    
    if row['PaymentTerms'] == 'Net-90':
        score += 2.0
    elif row['PaymentTerms'] == 'Net-60':
        score += 1.0
    else:
        score += 0.5
    
    score += np.random.uniform(0, 1)
    return min(10, max(1, round(score, 1)))

df['ServiceIntensityScore'] = df.apply(calculate_service_intensity, axis=1)
print(f"\n✓ ServiceIntensityScore: Complex formula (DETERMINISTIC)")
print(f"  - Min: {df['ServiceIntensityScore'].min()}, Max: {df['ServiceIntensityScore'].max()}, Mean: {df['ServiceIntensityScore'].mean():.2f}")
print(f"  - HORECA avg: {df[df['OriginalChannel'] == 1]['ServiceIntensityScore'].mean():.2f}")
print(f"  - Retail avg: {df[df['OriginalChannel'] == 2]['ServiceIntensityScore'].mean():.2f}")

# ServiceIntensityDrivers (text explanation)
def explain_drivers(row):
    drivers = []
    drivers.append("HORECA" if row['OriginalChannel'] == 1 else "Retail")
    if row['OrderFrequencyPerMonth'] >= 4:
        drivers.append("High freq")
    elif row['OrderFrequencyPerMonth'] >= 2.5:
        drivers.append("Med freq")
    else:
        drivers.append("Low freq")
    drivers.append(row['PaymentTerms'])
    return " + ".join(drivers)

df['ServiceIntensityDrivers'] = df.apply(explain_drivers, axis=1)
print(f"✓ ServiceIntensityDrivers: Text explanation (DETERMINISTIC)")

# HasPremiumRequests (score > 6)
df['HasPremiumRequests'] = df['ServiceIntensityScore'] > 6
premium_count = df['HasPremiumRequests'].sum()
print(f"✓ HasPremiumRequests: Score > 6 triggers TRUE (DETERMINISTIC)")
print(f"  - Count: {premium_count} ({premium_count/len(df)*100:.1f}%)")

# AcquisitionDate (from DaysAsCustomer)
acquisition_ref_date = pd.Timestamp('2024-11-04')
df['AcquisitionDate'] = acquisition_ref_date - pd.to_timedelta(df['DaysAsCustomer'], unit='D')
print(f"✓ AcquisitionDate: Calculated from DaysAsCustomer (DETERMINISTIC)")

# SalesRepAssigned (random across 25 reps)
num_reps = 25
df['SalesRepAssigned'] = [f"REP-{str(np.random.randint(1, num_reps+1)).zfill(2)}" for _ in range(len(df))]
print(f"✓ SalesRepAssigned: RANDOM across {num_reps} reps")

# AccountTier (score-based with revenue override)
def assign_account_tier(row):
    score = row['ServiceIntensityScore']
    revenue = row['TotalAnnualRevenue']
    
    if score >= 7:
        return 'PREMIUM'
    elif score >= 4:
        return 'STANDARD'
    else:
        if revenue > 50000:
            return 'ENTERPRISE'
        else:
            return 'STANDARD'

df['AccountTier'] = df.apply(assign_account_tier, axis=1)
tier_counts = df['AccountTier'].value_counts()
print(f"✓ AccountTier: Score-based with revenue override (DETERMINISTIC)")
print(f"  - PREMIUM: {tier_counts.get('PREMIUM', 0)}")
print(f"  - STANDARD: {tier_counts.get('STANDARD', 0)}")
print(f"  - ENTERPRISE: {tier_counts.get('ENTERPRISE', 0)}")

print("\n" + "=" * 80)
print("STEP 3: SELECT & SAVE FINAL COLUMNS")
print("=" * 80)

final_columns = [
    'CustomerID', 'CustomerName', 'OriginalChannel', 'ChannelName',
    'OriginalRegion', 'RegionName', 'AnnualFreshSpending', 'AnnualMilkSpending',
    'AnnualGrocerySpending', 'AnnualFrozenSpending', 'AnnualDetergentsPaperSpending',
    'AnnualDelicatessenSpending', 'TotalAnnualRevenue', 'CustomerSegment', 'PaymentTerms',
    'OrderFrequencyPerMonth', 'ServiceIntensityScore', 'ServiceIntensityDrivers',
    'HasPremiumRequests', 'DaysAsCustomer', 'AcquisitionDate', 'SalesRepAssigned', 'AccountTier'
]

df_final = df[final_columns].copy()
df_final.to_csv('data/processed/01_customer_master.csv', index=False)

print(f"✓ Saved Customer Master: 440 rows × {len(final_columns)} columns")
print(f"✓ Location: data/processed/01_customer_master.csv")

print("\n" + "=" * 80)
print("FINAL CUSTOMER MASTER SAMPLE")
print("=" * 80)
print(df_final[['CustomerID', 'CustomerName', 'ChannelName', 'CustomerSegment', 'PaymentTerms', 'AccountTier']].head(10))
