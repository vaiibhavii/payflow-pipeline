import duckdb, json

conn = duckdb.connect('payflow_bronze.duckdb')

# UPI trend data
rows = conn.execute("""
    SELECT month_year, total_volume_millions, average_daily_volume_millions
    FROM gold_layer.monthly_business_metrics
    ORDER BY month_year
""").fetchall()

data = [{"month": r[0], "volume": r[1], "avg_daily": r[2]} for r in rows]

with open('dashboard/data.json', 'w') as f:
    json.dump(data, f)

print(f"Exported {len(data)} records to dashboard/data.json")
conn.close()