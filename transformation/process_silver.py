import duckdb

def process_silver_layer():
    print("Starting Silver Layer Transformation...")
    
    # 1. Connect to your local database
    conn = duckdb.connect('payflow_bronze.duckdb')
    
    # 2. SQL to clean and transform the EXACT columns we found
    transform_query = """
    CREATE SCHEMA IF NOT EXISTS silver_layer;
    
    CREATE OR REPLACE TABLE silver_layer.cleaned_upi AS 
    SELECT 
        month AS month_year,
        CAST(REPLACE(volume_in_mnx, ',', '') AS FLOAT) AS volume_mn,
        avg_daily_volume_in_mnx AS avg_daily_volume_mn
    FROM raw_upi_data.stg_raw_upi
    WHERE month IS NOT NULL;
    """
    
    try:
        conn.execute(transform_query)
        
        # 3. Verify the transformation
        count = conn.execute("SELECT COUNT(*) FROM silver_layer.cleaned_upi").fetchone()[0]
        print(f"✅ Silver layer processing complete! {count} clean records loaded into 'silver_layer.cleaned_upi'.")
        
    except Exception as e:
        print(f"❌ Error during transformation: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    process_silver_layer()