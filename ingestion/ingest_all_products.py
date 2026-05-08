import pandas as pd
import duckdb
import os
import numpy as np

conn = duckdb.connect('payflow_bronze.duckdb')
conn.execute("CREATE SCHEMA IF NOT EXISTS raw_data")

files = {
    "upi": "data/raw/UPI Monthly Product Statistics Trended.csv",
    "imps": "data/raw/IMPS Monthly Product Statistics Trended.csv"
}

BANKS = ['SBI', 'HDFC', 'ICICI', 'Axis', 'HDFC', 'PNB', 'Canara']
REGIONS = ['North', 'South', 'East', 'West', 'Central']

for name, path in files.items():
    if os.path.exists(path):
        df = pd.read_csv(path)
        df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]
        
        # --- THE EXPLOSION LOGIC ---
        # We multiply every month by Banks and Regions
        dfs = []
        for bank in BANKS:
            for region in REGIONS:
                temp_df = df.copy()
                temp_df['bank'] = bank
                temp_df['region'] = region
                # Add slight random noise to volumes so they aren't identical
                if 'total_volume_millions' in temp_df.columns:
                    temp_df['total_volume_millions'] = temp_df['total_volume_millions'] * np.random.uniform(0.8, 1.2)
                dfs.append(temp_df)
        
        large_df = pd.concat(dfs, ignore_index=True)
        
        # To get to "Tons", we repeat this for 100 'Virtual Days' per month
        final_list = [large_df] * 50 
        tons_of_data = pd.concat(final_list, ignore_index=True)

        conn.execute(f"CREATE OR REPLACE TABLE raw_data.stg_{name} AS SELECT * FROM tons_of_data")
        print(f"🚀 EXPLODED {name}: {len(tons_of_data):,} rows created in Bronze.")

conn.close()