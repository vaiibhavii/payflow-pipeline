import duckdb

conn = duckdb.connect('payflow_bronze.duckdb')

# Create the Gold Layer Schema
conn.execute("CREATE SCHEMA IF NOT EXISTS gold_layer")

# This SQL aggregates the REAL records you just cloned from GitHub
conn.execute("""
CREATE OR REPLACE TABLE gold_layer.phonepe_metrics AS
SELECT 
    year || '-Q' || quarter as period,
    SUM(count) / 1000000.0 as volume_millions,
    SUM(amount) / 10000000.0 as value_cr
FROM raw_data.stg_phonepe
GROUP BY year, quarter
ORDER BY year ASC, quarter ASC
""")

print(f"✅ Gold Layer updated with {conn.execute('SELECT count(*) FROM gold_layer.phonepe_metrics').fetchone()[0]} real data points.")
conn.close()