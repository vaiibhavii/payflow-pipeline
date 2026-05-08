import os
import subprocess
import duckdb
import pandas as pd

# 1. Clone the REAL dataset from PhonePe's official repo
repo_url = "https://github.com/PhonePe/pulse.git"
dest_path = "data/phonepe_pulse"

if not os.path.exists(dest_path):
    print("🚀 Cloning real PhonePe Pulse data...")
    subprocess.run(["git", "clone", repo_url, dest_path])

# 2. Ingesting Aggregated Transaction Data (Real Files)
con = duckdb.connect('payflow_bronze.duckdb')
con.execute("CREATE SCHEMA IF NOT EXISTS raw_data")

# Path to the real JSON data in the cloned repo
base_path = "data/phonepe_pulse/data/aggregated/transaction/country/india/state/"
all_records = []

print("📂 Processing real state-level records...")
for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        for file in os.listdir(year_path):
            with open(os.path.join(year_path, file), 'r') as f:
                import json
                data = json.load(f)
                for item in data['data']['transactionData']:
                    all_records.append({
                        'state': state,
                        'year': year,
                        'quarter': file.replace('.json', ''),
                        'transaction_type': item['name'],
                        'count': item['paymentInstruments'][0]['count'],
                        'amount': item['paymentInstruments'][0]['amount']
                    })

# 3. Load into Bronze
df = pd.DataFrame(all_records)
con.execute("CREATE OR REPLACE TABLE raw_data.stg_phonepe AS SELECT * FROM df")

# 4. Persistence to MinIO
os.makedirs('data/lake', exist_ok=True)
con.execute("COPY raw_data.stg_phonepe TO 'data/lake/phonepe_real_data.parquet' (FORMAT PARQUET)")

print(f"✅ Real Data Ingested: {len(df)} records from PhonePe Pulse.")
con.close() 