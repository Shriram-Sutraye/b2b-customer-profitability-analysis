from google.cloud import bigquery

client = bigquery.Client(project='flawless-energy-473422-k4')

# Get schema of financial_p_l_orders table
table = client.get_table('flawless-energy-473422-k4.b2b_profitability.financial_p_l_orders')

print("📋 Column names in financial_p_l_orders:\n")
for field in table.schema:
    print(f"  • {field.name} ({field.field_type})")
