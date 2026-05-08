import duckdb
conn = duckdb.connect('payflow_bronze.duckdb')

# We use SUM() and GROUP BY to merge those duplicate months into one data point
conn.execute("""
CREATE OR REPLACE TABLE gold_layer.monthly_business_metrics AS
SELECT 
    month_year as month,
    SUM(volume_mn) as volume
FROM silver_layer.cleaned_upi
GROUP BY month_year
ORDER BY month_year ASC
""")

conn.close()
print("✅ Gold Layer Fixed: Monthly totals aggregated.")