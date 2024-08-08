# Script to list the size of all S3 buckets across all AWS accounts in an AWS Organization
import boto3
import json

# Initialize the boto3 clients
org_client = boto3.client('organizations')
sts_client = boto3.client('sts')
s3_client = boto3.client('s3')

def assume_role(account_id, role_name):
    response = sts_client.assume_role(
        RoleArn=f'arn:aws:iam::{account_id}:role/S3ListBucketRole',
        RoleSessionName='S3BucketSizeCheck'
    )
    credentials = response['Credentials']
    return boto3.client(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )

def get_accounts():
    paginator = org_client.get_paginator('list_accounts')
    accounts = []
    for page in paginator.paginate():
        accounts.extend(page['Accounts'])
    return accounts

def get_bucket_size(s3_client, bucket_name):
    total_size = 0
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            total_size += obj['Size']
    return total_size

def main():
    role_name = 'YourAssumeRoleName'
    accounts = get_accounts()
    for account in accounts:
        account_id = account['Id']
        print(f'Checking account: {account_id}')
        try:
            s3_client = assume_role(account_id, role_name)
            response = s3_client.list_buckets()
            for bucket in response['Buckets']:
                bucket_name = bucket['Name']
                size = get_bucket_size(s3_client, bucket_name)
                print(f'Account: {account_id}, Bucket: {bucket_name}, Size: {size / (1024 ** 3):.2f} GB')
        except Exception as e:
            print(f'Could not process account {account_id}: {e}')

if __name__ == '__main__':
    main()
