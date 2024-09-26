import boto3
s3 = boto3.client('s3')


def find_objects_with_archive_status(bucket_name):
    paginator = s3.get_paginator('list_objects_v2')
    response_iterator = paginator.paginate(Bucket=bucket_name)
# Change the above line if you want to define a prefix
    #response_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
  for page in response_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                object_key = obj['Key']

                head_response = s3.head_object(Bucket=bucket_name, Key=object_key)

                storageclass = head_response.get('StorageClass')
                if storageclass == "INTELLIGENT_TIERING":
                            archive_status = head_response.get('ArchiveStatus')
                            print(archive_status)
                            if archive_status == "ARCHIVE_ACCESS":
                                print(object_key)
                                print("found glacier object")
                                response = s3.restore_object(
                                    Bucket=bucket_name,
                                    Key=object_key,
                                    RestoreRequest={
                                        'GlacierJobParameters': {
                                            'Tier': 'Standard',
                                        },
                                    },
                                )


bucket_name = 'mybucket-name'
#prefix = 'some/path/in/bucket'
find_objects_with_archive_status(bucket_name)
