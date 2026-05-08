import duckdb
import os

# 1. Create the directory structure
os.makedirs('data/lake', exist_ok=True)

# 2. Connect to DuckDB
conn = duckdb.connect('payflow_bronze.duckdb')

print("📤 Exporting tables to Parquet for MinIO...")

try:
    # Export the PhonePe data if you ran that script
    conn.execute("COPY raw_data.stg_phonepe TO 'data/lake/phonepe_real_data.parquet' (FORMAT PARQUET)")
    print("✅ Exported phonepe_real_data.parquet")
except Exception as e:
    # If PhonePe isn't there, export the Kaggle raw data instead
    print(f"⚠️ PhonePe table not found, exporting Kaggle data instead: {e}")
    conn.execute("COPY raw_upi_data.stg_raw_upi TO 'data/lake/phonepe_real_data.parquet' (FORMAT PARQUET)")
    print("✅ Exported stg_raw_upi as the bronze file.")

conn.close()