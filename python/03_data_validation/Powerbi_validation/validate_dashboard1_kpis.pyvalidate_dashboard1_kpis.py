import pandas as pd

df = pd.read_csv('data/generated/11_customer_lifetime_value.csv')
# Proper calculation for gross margin %
gross_margin_pct = df['CLVMargin_Pct'].mean()

print(f"Gross Margin %: {gross_margin_pct:.2f}%")

# Annual Profit by CLV Segment
segment_profit = df.groupby('CLVSegment')['AnnualProfit_EUR'].sum()
for seg, profit in segment_profit.items():
    print(f"{seg}: {profit/1e6:.1f}M EUR")