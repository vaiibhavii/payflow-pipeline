import duckdb
import json
import os

conn = duckdb.connect('payflow_bronze.duckdb')

# Query the REAL aggregates
rows = conn.execute("""
    SELECT period, volume_millions, value_cr 
    FROM gold_layer.phonepe_metrics
""").fetchall()

# Format for Chart.js
data = [
    {"month": r[0], "volume": round(r[1], 2), "value": round(r[2], 2)} 
    for r in rows
]

os.makedirs('dashboard', exist_ok=True)
with open('dashboard/data.json', 'w') as f:
    json.dump(data, f, indent=4)

print(f"🚀 Dashboard Refreshed! {len(data)} REAL data points pushed to UI.")
conn.close()