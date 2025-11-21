from google.cloud import bigquery
import pandas as pd

client = bigquery.Client(project='flawless-energy-473422-k4')

# Query 1: Total revenue and profit
query1 = """
SELECT 
    ROUND(SUM(TransactionAmount), 2) as total_revenue,
    ROUND(SUM(Profit_EUR), 2) as total_profit,
    ROUND(SUM(Profit_EUR) / SUM(TransactionAmount) * 100, 2) as margin_pct,
    COUNT(*) as total_transactions
FROM `flawless-energy-473422-k4.b2b_profitability.financial_p_l_orders`
"""

print("💰 Revenue & Profit Summary:")
df1 = client.query(query1).to_dataframe()
print(df1)
print(f"\n   Total Revenue: €{df1['total_revenue'][0]:,.2f}")
print(f"   Total Profit:  €{df1['total_profit'][0]:,.2f}")
print(f"   Margin:        {df1['margin_pct'][0]:.2f}%")

# Query 2: Top 10 customers by CLV
query2 = """
SELECT 
    CustomerID,
    ROUND(CLV_EUR, 2) as CLV,
    CLVSegment,
    AnnualProfit_EUR,
    OrderCount
FROM `flawless-energy-473422-k4.b2b_profitability.customer_lifetime_value`
ORDER BY CLV_EUR DESC
LIMIT 10
"""

print("\n📈 Top 10 Customers by CLV:")
print(client.query(query2).to_dataframe().to_string(index=False))

# Query 3: Customer segment breakdown
query3 = """
SELECT 
    CLVSegment,
    COUNT(*) as customer_count,
    ROUND(SUM(CLV_EUR), 2) as total_clv,
    ROUND(AVG(CLV_EUR), 2) as avg_clv
FROM `flawless-energy-473422-k4.b2b_profitability.customer_lifetime_value`
GROUP BY CLVSegment
ORDER BY total_clv DESC
"""

print("\n🎯 Customer Segmentation:")
print(client.query(query3).to_dataframe().to_string(index=False))

# Query 4: Profitability by segment
query4 = """
SELECT 
    CustomerSegment,
    COUNT(*) as order_count,
    ROUND(SUM(TransactionAmount), 2) as revenue,
    ROUND(SUM(Profit_EUR), 2) as profit,
    ROUND(AVG(ProfitMargin_Pct), 2) as avg_margin_pct
FROM `flawless-energy-473422-k4.b2b_profitability.financial_p_l_orders`
GROUP BY CustomerSegment
ORDER BY profit DESC
"""

print("\n💼 Profitability by Customer Segment:")
print(client.query(query4).to_dataframe().to_string(index=False))

print("\n✅ All queries executed successfully! BigQuery data is ready for analysis.")
