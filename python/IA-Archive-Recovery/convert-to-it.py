import boto3
from tqdm import tqdm

# Initialize the S3 client
s3_client = boto3.client('s3')

# Retrieve list of S3 bucket names
s3_resource = boto3.resource('s3')
bucket_names = [bucket.name for bucket in s3_resource.buckets.all()]

# Lifecycle configuration
lifecycle_configuration = {
    "Rules": [{
        "ID": "Intelligent Tiering",
        "Filter": {},
        "Status": "Enabled",
        "Transitions": [{"Days": 0, "StorageClass": "INTELLIGENT_TIERING"}],
        "NoncurrentVersionTransitions": [{
            "NoncurrentDays": 0,
            "StorageClass": "INTELLIGENT_TIERING"
        }]
    }]
}

# Apply the lifecycle policy to each bucket
for bucket_name in tqdm(bucket_names, desc="Processing buckets"):
    try:
        s3_client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_configuration
        )
        print(f"Lifecycle policy added to S3 bucket: {bucket_name}")
    except Exception as e:
        print(f"Failed to add lifecycle policy to {bucket_name}: {e}")

