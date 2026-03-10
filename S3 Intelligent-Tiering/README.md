# S3 Intelligent-Tiering Assessment Tool

Analyze local directories or S3 buckets to determine if your dataset is a good candidate for AWS S3 Intelligent-Tiering storage class.

## What is S3 Intelligent-Tiering?

S3 Intelligent-Tiering automatically moves objects between access tiers based on usage patterns, optimizing storage costs without performance impact. It works best for:
- Large files (>128KB recommended)
- Unpredictable or changing access patterns
- Long-term storage with varying access frequency

## Installation

```bash
# Clone or download this repository
cd s3-tiering-assesment

# Ensure Python 3.6+ is installed
python3 --version

# For S3 bucket analysis only: Install boto3
pip install boto3
```

**Dependencies:**
- **Local directory analysis**: No dependencies (uses Python standard library only)
- **S3 bucket analysis**: Requires `boto3` library

## Usage

### Local Directory Analysis

```bash
python3 local_tiering_analyzer.py <directory_path>
```

**Example:**
```bash
python3 local_tiering_analyzer.py /path/to/your/data
```

### S3 Bucket Analysis

```bash
python3 s3_tiering_analyzer.py <bucket-name> [prefix]
```

**Examples:**
```bash
# Analyze entire bucket
python3 s3_tiering_analyzer.py my-bucket

# Analyze specific prefix/folder
python3 s3_tiering_analyzer.py my-bucket data/archive/
```

**AWS Configuration:**
Ensure AWS credentials are configured before running:
```bash
aws configure
```

### Interrupting the Scan

Press `Ctrl+C` at any time to stop the scan and view results for objects/files processed so far.

## Output

The tool provides:
- **Live Progress**: Real-time file count, total size, and current file being processed
- **Size Distribution**: Files categorized into tiny (<128KB), small (128KB-1MB), medium (1MB-100MB), and large (>100MB)
- **Recommendation**: Assessment of whether your dataset is suitable for Intelligent-Tiering

### Sample Output

```
🔍 Scanning: /path/to/data

📄 Files: 1,523 | Size: 45.32 GB | Current: large_video_file.mp4

======================================================================
📊 S3 INTELLIGENT-TIERING ANALYSIS
======================================================================
Total Files: 1,523
Total Size: 45.32 GB
Scan Time: 12.45s

File Size Distribution:
----------------------------------------------------------------------
  Tiny     |      234 files (15.4%) | 18.45 MB
  Small    |      189 files (12.4%) | 142.67 MB
  Medium   |      856 files (56.2%) | 23.12 GB
  Large    |      244 files (16.0%) | 22.03 GB

======================================================================
💡 RECOMMENDATION
======================================================================
✅ EXCELLENT CANDIDATE - Majority are medium/large files
   Intelligent-Tiering will optimize costs based on access patterns.
======================================================================
```

## Recommendation Criteria

- **✅ Excellent**: >60% medium/large files - ideal for Intelligent-Tiering
- **⚠️ Moderate**: Mixed distribution - consider filtering or lifecycle policies
- **❌ Not Recommended**: >70% tiny files - per-request costs outweigh benefits

## IAM Permissions for S3 Analysis

The S3 analyzer requires minimal read-only permissions. Create an IAM policy with:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name"
    }
  ]
}
```

**Cost Optimization:**
- Uses `ListObjectsV2` API only (no data transfer)
- Only reads object metadata (size, key)
- Does not download or access object contents
- Typical cost: $0.005 per 1,000 requests

## Notes

**Local Directory Analysis:**
- Skips files it cannot access (permission errors)
- Symbolic links are followed by default
- Hidden files and directories are included in the scan

**S3 Bucket Analysis:**
- Only reads object metadata (no data transfer costs)
- Requires `s3:ListBucket` permission
- Works with buckets in any region
- Results are based on current object sizes, not access patterns

## License

MIT
