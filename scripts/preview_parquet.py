import pandas as pd

# Read the local copy of the file we uploaded to MinIO
file_path = 'data/lake/phonepe_real_data.parquet'

if os.path.exists(file_path):
    df = pd.read_parquet(file_path)
    print("👀 PARQUET DATA PREVIEW (First 10 Rows):")
    print(df.head(10).to_string())
    print(f"\n✅ Total Columns: {len(df.columns)}")
    print(f"✅ Schema: {df.dtypes.to_dict()}")
else:
    print("❌ Parquet file not found on disk. Run export_for_minio.py first.")