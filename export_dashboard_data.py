"""
PayFlow — Export Gold Layer to dashboard/data.json
Place this in: D:/payflow-pipeline/   (project ROOT)
Run: python export_dashboard_data.py
"""

import duckdb
import json
import os

conn = duckdb.connect('payflow_bronze.duckdb')
os.makedirs('dashboard', exist_ok=True)

print("📤 Exporting Gold layer to dashboard/data.json...")

# Try Gold layer first (from process_gold.py output)
try:
    rows = conn.execute("""
        SELECT month_year, total_volume_millions, average_daily_volume_millions
        FROM gold_layer.monthly_business_metrics
        ORDER BY month_year
    """).fetchall()

    data = [
        {
            "month": r[0],
            "volume": round(float(r[1]), 2),
            "avg_daily": round(float(r[2]), 2)
        }
        for r in rows
    ]
    source = "gold_layer.monthly_business_metrics"

except Exception as e:
    print(f"⚠️  Gold layer not ready ({e}), falling back to Silver...")
    try:
        rows = conn.execute("""
            SELECT month_year, volume_mn, avg_daily_volume_mn
            FROM silver_layer.cleaned_upi
            ORDER BY month_year
        """).fetchall()
        data = [
            {"month": r[0], "volume": round(float(r[1]),2), "avg_daily": round(float(r[2]),2)}
            for r in rows
        ]
        source = "silver_layer.cleaned_upi"
    except Exception as e2:
        print(f"⚠️  Silver not ready ({e2}), using Bronze raw data...")
        rows = conn.execute("""
            SELECT month, volume_in_mnx, avg_daily_volume_in_mnx
            FROM raw_upi_data.stg_raw_upi
        """).fetchall()
        data = [
            {"month": r[0], "volume": float(str(r[1]).replace(',','')), "avg_daily": float(r[2])}
            for r in rows
        ]
        source = "raw_upi_data.stg_raw_upi"

with open('dashboard/data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Exported {len(data)} records from [{source}] → dashboard/data.json")
conn.close()