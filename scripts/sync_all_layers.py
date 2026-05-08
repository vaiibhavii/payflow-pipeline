import boto3
import duckdb
import os

s3 = boto3.client('s3', 
    endpoint_url='http://localhost:9000', 
    aws_access_key_id='payflow', 
    aws_secret_access_key='payflow123'
)

# 1. Export Gold Data from DuckDB
conn = duckdb.connect('payflow_bronze.duckdb')
os.makedirs('data/lake', exist_ok=True)

try:
    # Exporting your monthly metrics to a parquet file for the Gold bucket
    conn.execute("COPY (SELECT * FROM gold_layer.monthly_business_metrics) TO 'data/lake/gold_metrics.parquet' (FORMAT PARQUET)")
    print("✅ Exported Gold Parquet")
except Exception as e:
    print(f"⚠️ Gold table not ready yet: {e}")

# 2. Upload to respective buckets
layers = {
    'bronze': 'data/lake/phonepe_real_data.parquet',
    'silver': 'data/lake/phonepe_real_data.parquet', # Using as a placeholder
    'gold': 'data/lake/gold_metrics.parquet'
}

for bucket, path in layers.items():
    if os.path.exists(path):
        s3.upload_file(path, bucket, os.path.basename(path))
        print(f"🚀 Synced {bucket} bucket")

conn.close()