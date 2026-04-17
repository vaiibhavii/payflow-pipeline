import duckdb

def process_gold_layer():
    print("Starting Gold Layer Transformation (Business Metrics)...")
    
    conn = duckdb.connect('payflow_bronze.duckdb')
    
    # We create a Gold schema and a table ready for business reporting
    gold_query = """
    CREATE SCHEMA IF NOT EXISTS gold_layer;
    
    CREATE OR REPLACE TABLE gold_layer.monthly_business_metrics AS 
    SELECT 
        month_year,
        volume_mn AS total_volume_millions,
        avg_daily_volume_mn AS average_daily_volume_millions,
        -- Creating a derived metric for the dashboard
        (volume_mn * 1000000) AS actual_volume_count 
    FROM silver_layer.cleaned_upi
    ORDER BY month_year DESC;
    """
    
    try:
        conn.execute(gold_query)
        
        # Verify the Gold layer
        count = conn.execute("SELECT COUNT(*) FROM gold_layer.monthly_business_metrics").fetchone()[0]
        print(f"✅ Gold layer processing complete! {count} business-ready records loaded into 'gold_layer.monthly_business_metrics'.")
        
    except Exception as e:
        print(f"❌ Error during Gold transformation: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    process_gold_layer()