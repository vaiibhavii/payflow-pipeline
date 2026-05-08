import boto3
import os

# Initialize the S3 client pointing to your local MinIO
s3 = boto3.client('s3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='payflow',
    aws_secret_access_key='payflow123'
)

def upload_layers():
    # Paths to your exported data (or your raw CSVs)
    files_to_upload = {
        'bronze': 'data/raw/UPI Monthly Product Statistics Trended.csv',
        'silver': 'dashboard/data.json', # Just as a placeholder for now
    }

    for bucket, file_path in files_to_upload.items():
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            s3.upload_file(file_path, bucket, file_name)
            print(f"✅ Successfully uploaded {file_name} to {bucket} bucket.")
        else:
            print(f"⚠️ Could not find {file_path}")

if __name__ == "__main__":
    try:
        upload_layers()
    except Exception as e:
        print(f"❌ MinIO Connection Failed: {e}")