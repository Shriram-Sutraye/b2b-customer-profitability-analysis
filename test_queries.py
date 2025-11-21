from google.cloud import bigquery
import pandas as pd

client = bigquery.Client(project='flawless-energy-473422-k4')

# Query 1: Total revenue and profit
query1 = """
SELECT 
    ROUND(SUM(TRANSACTION_AMOUNT), 2) as total_revenue,
    ROUND(SUM(PROFIT_EUR), 2) as total_profit,
    ROUND(SUM(PROFIT_EUR) / SUM(TRANSACTION_AMOUNT) * 100, 2) as margin_pct
FROM `flawless-energy-473422-k4.b2b_profitability.financial_p_l_orders`
"""

print("💰 Revenue & Profit Summary:")
print(client.query(query1).to_dataframe())

# Query 2: Top 10 customers by CLV
query2 = """
SELECT 
    CUSTOMERID,
    ROUND(CLV_EUR, 2) as CLV,
    CLVSEGMENT
FROM `flawless-energy-473422-k4.b2b_profitability.customer_lifetime_value`
ORDER BY CLV_EUR DESC
LIMIT 10
"""

print("\n📈 Top 10 Customers by CLV:")
print(client.query(query2).to_dataframe())

# Query 3: Customer segment breakdown
query3 = """
SELECT 
    CLVSEGMENT,
    COUNT(*) as customer_count,
    ROUND(SUM(CLV_EUR), 2) as total_clv
FROM `flawless-energy-473422-k4.b2b_profitability.customer_lifetime_value`
GROUP BY CLVSEGMENT
ORDER BY total_clv DESC
"""

print("\n🎯 Customer Segmentation:")
print(client.query(query3).to_dataframe())
