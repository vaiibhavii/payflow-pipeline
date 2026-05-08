import duckdb
import json
import os

# 1. Establish the connection to your existing database
# Ensure this path matches where your .duckdb file is located
db_path = 'payflow_bronze.duckdb'

if not os.path.exists(db_path):
    print(f"❌ Error: {db_path} not found. Run your ingestion scripts first!")
else:
    conn = duckdb.connect(db_path)
    print("✅ Connected to PayFlow Database")

    try:
        # 2. Extract Gold Layer metrics
        # Adjust the table name if yours is different (e.g., gold_layer.monthly_business_metrics)
        query = """
            SELECT month_year, total_volume_millions, average_daily_volume_millions
            FROM gold_layer.monthly_business_metrics
            ORDER BY month_year
        """
        
        rows = conn.execute(query).fetchall()

        # 3. Format for the Dashboard
        data = [{"month": r[0], "volume": r[1], "avg_daily": r[2]} for r in rows]

        # 4. Save to JSON in the dashboard folder
        os.makedirs('dashboard', exist_ok=True)
        with open('dashboard/data.json', 'w') as f:
            json.dump(data, f, indent=4)

        print(f"🚀 Exported {len(data)} records to dashboard/data.json")

    except Exception as e:
        print(f"❌ Query failed: {e}")
    
    finally:
        conn.close()