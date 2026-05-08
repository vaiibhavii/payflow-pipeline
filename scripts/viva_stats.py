import duckdb

conn = duckdb.connect('payflow_bronze.duckdb')

# Show the massive scale you ingested
print("📊 PIPELINE VOLUME AUDIT")
print("-" * 30)
layers = {
    "BRONZE (Raw)": "raw_data.stg_upi",
    "SILVER (Clean)": "silver_layer.cleaned_upi",
    "GOLD (Aggregated)": "gold_layer.monthly_business_metrics"
}

for label, table in layers.items():
    try:
        count = conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        print(f"{label}: {count:,} rows")
    except:
        print(f"{label}: Not found or empty")

conn.close()