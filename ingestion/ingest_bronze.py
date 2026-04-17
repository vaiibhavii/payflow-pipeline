import pandas as pd
import dlt
import kaggle
import os

def load_raw_data():
    # 1. Automated Download
    dataset = "nilesh2042/monthly-metrics"
    kaggle.api.dataset_download_files(dataset, path='data/raw', unzip=True)

    # 2. Pipeline Configuration
    pipeline = dlt.pipeline(
        pipeline_name="payflow_bronze",
        destination="duckdb",
        dataset_name="raw_upi_data"
    )
    
    # 3. Read CSV with Pandas (Fixes the 'InvalidResourceDataType' error)
    csv_path = "data/raw/UPI Monthly Product Statistics Trended.csv"
    df = pd.read_csv(csv_path)
    
    # 4. Ingest to Bronze (Naming the table stg_raw_upi as per your Chapter 2.3)
    info = pipeline.run(df, table_name="stg_raw_upi")
    print(info)

if __name__ == "__main__":
    load_raw_data()