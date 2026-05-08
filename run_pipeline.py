import subprocess
import time

def run_step(command, description):
    print(f"🔄 {description}...")
    result = subprocess.run(command, shell=True)
    if result.returncode == 0:
        print(f"✅ {description} Successful")
    else:
        print(f"❌ {description} Failed")

if __name__ == "__main__":
    print("🚀 STARTING PAYFLOW MASTER PIPELINE")
    print("="*40)
    
    # Step 1: Ingest Raw Data
    run_step("python ingestion/ingest_bronze.py", "Ingesting Bronze Layer")
    
    # Step 2: Transform to Silver (Cleaning)
    run_step("python transformation/process_silver.py", "Processing Silver Layer")
    
    # Step 3: Transform to Gold (Aggregating)
    run_step("python transformation/process_gold.py", "Processing Gold Layer")
    
    # Step 4: Export for Dashboard
    run_step("python export_dashboard_data.py", "Refreshing Dashboard Data")
    
    # Step 5: Sync to MinIO
    run_step("python scripts/upload_to_minio.py", "Syncing to Object Storage")
    
    print("="*40)
    print("🏁 PIPELINE COMPLETE. Refresh your browser to see updates.")