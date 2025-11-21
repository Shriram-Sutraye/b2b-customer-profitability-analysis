from google.cloud import bigquery

client = bigquery.Client(project='flawless-energy-473422-k4')

# List all tables in dataset
tables = client.list_tables('b2b_profitability')
print("📊 Tables in BigQuery:\n")
for table in tables:
    full_table = client.get_table(f"flawless-energy-473422-k4.b2b_profitability.{table.table_id}")
    print(f"✅ {table.table_id:40} | {full_table.num_rows:,} rows | {full_table.num_bytes/1024/1024:.2f} MB")
