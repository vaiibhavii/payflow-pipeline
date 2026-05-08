import boto3
from botocore.exceptions import NoCredentialsError

s3 = boto3.client('s3', 
    endpoint_url='http://localhost:9000', 
    aws_access_key_id='payflow', 
    aws_secret_access_key='payflow123'
)

source_file = 'data/lake/phonepe_real_data.parquet'
bucket_name = 'bronze'
object_name = 'phonepe_real_data.parquet'

try:
    # Check if bucket exists first
    s3.head_bucket(Bucket=bucket_name)
    print(f"✅ Bucket '{bucket_name}' found.")
    
    # Upload
    s3.upload_file(source_file, bucket_name, object_name)
    print(f"🚀 SUCCESS: {object_name} is now in MinIO.")
    
    # Verify by listing
    response = s3.list_objects_v2(Bucket=bucket_name)
    print(f"📂 Current files in {bucket_name}: {[obj['Key'] for obj in response.get('Contents', [])]}")

except Exception as e:
    print(f"❌ ERROR: {str(e)}")