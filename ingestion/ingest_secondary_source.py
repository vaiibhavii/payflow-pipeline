import pandas as pd
import duckdb
import os

# Simulated RBI source data
data_v2 = {
    'month_year': ['2024-01', '2024-02', '2024-03', '2024-04'],
    'volume_mn': [450.5, 480.2, 510.8, 540.3],
    'source_system': ['RBI_RTGS', 'RBI_RTGS', 'RBI_RTGS', 'RBI_RTGS']
}

df_rbi = pd.DataFrame(data_v2)
conn = duckdb.connect('payflow_bronze.duckdb')
conn.execute("CREATE SCHEMA IF NOT EXISTS raw_data_secondary")
conn.execute("CREATE OR REPLACE TABLE raw_data_secondary.stg_rbi_metrics AS SELECT * FROM df_rbi")

print(f"✅ Secondary source ingested into DuckDB.")
conn.close()