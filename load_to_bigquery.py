from google.cloud import bigquery
import time

client = bigquery.Client(project='flawless-energy-473422-k4')

# List of files to load
files = [
    ('01_customer_master.csv', 'customer_master'),
    ('02_transactions_generated.csv', 'transactions'),
    ('03_products_generated.csv', 'products'),
    ('04_warehouse_costs_generated.csv', 'warehouse_costs'),
    ('05_shipping_costs_generated.csv', 'shipping_costs'),
    ('06_returns_handling_generated.csv', 'returns_handling'),
    ('07_payment_terms_interest_generated.csv', 'payment_terms_interest'),
    ('09_admin_overhead_generated.csv', 'admin_overhead'),
    ('10_financial_p_l_orders.csv', 'financial_p_l_orders'),
    ('10_p_l_by_product.csv', 'p_l_by_product'),
    ('10_p_l_by_segment.csv', 'p_l_by_segment'),
    ('10_p_l_overall_summary.csv', 'p_l_overall_summary'),
    ('10_p_l_segment_product_matrix.csv', 'p_l_segment_product_matrix'),
    ('11_clv_action_summary.csv', 'clv_action_summary'),
    ('11_clv_by_segment_summary.csv', 'clv_by_segment_summary'),
    ('11_clv_segment_summary.csv', 'clv_segment_summary'),
    ('11_customer_lifetime_value.csv', 'customer_lifetime_value'),
    ('14_scenario_planning.csv', 'scenario_planning'),
]

for file, table_name in files:
    print(f"Loading {file} → {table_name}...")
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,  # Auto-detect schema
        write_disposition='WRITE_TRUNCATE'
    )
    
    uri = f"gs://flawless-energy-473422-k4-data/b2b/{file}"
    table_id = f"flawless-energy-473422-k4.b2b_profitability.{table_name}"
    
    start = time.time()
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()  # Wait for completion
    
    table = client.get_table(table_id)
    print(f"✅ Loaded {table.num_rows:,} rows in {time.time()-start:.1f}s")

print("\n🎉 All tables loaded successfully!")
