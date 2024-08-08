#!/bin/bash

# Check if AWS region is provided as a command-line argument
if [ -z "$1" ]; then
    echo "Usage: $0 <AWS_REGION>"
    exit 1
fi
# Account ID from were he script is running
your_account_id='XXXXXXXXXXXX'
# Extract AWS region from command-line argument
AWS_REGION="$1"

# Specify the key and value for the new tags
NEW_TAG_KEY="Tag-Name"
NEW_TAG_VALUE="Tag-value"

# Get a list of all EC2 instances
INSTANCE_IDS=$(aws ec2 describe-instances --region $AWS_REGION --query 'Reservations[*].Instances[*].InstanceId' --output text)

# Loop through each instance and apply the new tags
for instance_id in $INSTANCE_IDS; do
    echo "Applying tags to instance: $instance_id"
    aws ec2 create-tags --region $AWS_REGION --resources $instance_id --tags Key=$NEW_TAG_KEY,Value=$NEW_TAG_VALUE
done

# Get a list of all EBS volumes
VOLUME_IDS=$(aws ec2 describe-volumes --region $AWS_REGION --query 'Volumes[*].VolumeId' --output text)

# Loop through each volume and apply the new tags
for volume_id in $VOLUME_IDS; do
    echo "Applying tags to volume: $volume_id"
    aws ec2 create-tags --region $AWS_REGION --resources $volume_id --tags Key=$NEW_TAG_KEY,Value=$NEW_TAG_VALUE
done

# Get a list of all EBS snapshots
SNAPSHOT_IDS=$(aws ec2 describe-snapshots --region $AWS_REGION --owner-ids self --query 'Snapshots[*].SnapshotId' --output text)

# Loop through each snapshot and apply the new tags
for snapshot_id in $SNAPSHOT_IDS; do
    echo "Applying tags to EBS snapshot: $snapshot_id"
    aws ec2 create-tags --region $AWS_REGION --resources $snapshot_id --tags Key=$NEW_TAG_KEY,Value=$NEW_TAG_VALUE
done

# Get a list of all FSx filesystems
FSX_IDS=$(aws fsx describe-file-systems --region $AWS_REGION --query 'FileSystems[*].FileSystemId' --output text)

# Loop through each FSx filesystem and apply the new tags
for fsx_id in $FSX_IDS; do
    echo "Applying tags to FSx filesystem: $fsx_id"
    aws fsx tag-resource --region $AWS_REGION --resource-arn arn:aws:fsx:$AWS_REGION:$your_account_id:file-system/$fsx_id --tags Key=$NEW_TAG_KEY,Value=$NEW_TAG_VALUE
done

echo "Tagging complete."

