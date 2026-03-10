#!/usr/bin/env python3
import sys
import signal
from datetime import datetime

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
except ImportError:
    print("Error: boto3 is required. Install with: pip install boto3")
    sys.exit(1)

class S3TieringAnalyzer:
    def __init__(self):
        self.total_objects = 0
        self.total_size = 0
        self.size_buckets = {
            'tiny': {'count': 0, 'size': 0, 'max': 128 * 1024},
            'small': {'count': 0, 'size': 0, 'max': 1024 * 1024},
            'medium': {'count': 0, 'size': 0, 'max': 100 * 1024 * 1024},
            'large': {'count': 0, 'size': 0, 'max': float('inf')}
        }
        self.interrupted = False
        signal.signal(signal.SIGINT, self._handle_interrupt)
    
    def _handle_interrupt(self, sig, frame):
        self.interrupted = True
        print("\n\n⚠️  Interrupt received, generating summary...\n")
    
    def _categorize_object(self, size):
        for bucket, info in self.size_buckets.items():
            if size < info['max']:
                info['count'] += 1
                info['size'] += size
                return
    
    def _format_size(self, bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        return f"{bytes:.2f} PB"
    
    def scan(self, bucket_name, prefix=''):
        try:
            s3 = boto3.client('s3')
        except NoCredentialsError:
            print("Error: AWS credentials not found. Configure with 'aws configure'")
            sys.exit(1)
        
        print(f"🔍 Scanning S3 bucket: s3://{bucket_name}/{prefix}\n")
        start_time = datetime.now()
        
        paginator = s3.get_paginator('list_objects_v2')
        page_config = {'Bucket': bucket_name, 'Prefix': prefix}
        
        try:
            for page in paginator.paginate(**page_config):
                if self.interrupted:
                    break
                
                if 'Contents' not in page:
                    continue
                
                for obj in page['Contents']:
                    if self.interrupted:
                        break
                    
                    size = obj['Size']
                    self.total_objects += 1
                    self.total_size += size
                    self._categorize_object(size)
                    
                    key = obj['Key'].split('/')[-1] if '/' in obj['Key'] else obj['Key']
                    print(f"\r📦 Objects: {self.total_objects:,} | Size: {self._format_size(self.total_size)} | Current: {key[:50]}", end='', flush=True)
        
        except ClientError as e:
            print(f"\n\nError accessing bucket: {e}")
            sys.exit(1)
        
        print("\n")
        elapsed = (datetime.now() - start_time).total_seconds()
        self._print_summary(elapsed)
    
    def _print_summary(self, elapsed):
        print("=" * 70)
        print("📊 S3 INTELLIGENT-TIERING ANALYSIS")
        print("=" * 70)
        print(f"Total Objects: {self.total_objects:,}")
        print(f"Total Size: {self._format_size(self.total_size)}")
        print(f"Scan Time: {elapsed:.2f}s\n")
        
        print("Object Size Distribution:")
        print("-" * 70)
        for name, info in self.size_buckets.items():
            pct = (info['count'] / self.total_objects * 100) if self.total_objects > 0 else 0
            print(f"  {name.capitalize():8} | {info['count']:8,} objects ({pct:5.1f}%) | {self._format_size(info['size'])}")
        
        print("\n" + "=" * 70)
        print("💡 RECOMMENDATION")
        print("=" * 70)
        
        if self.total_objects == 0:
            print("⚠️  NO OBJECTS FOUND")
            print("=" * 70)
            return
        
        tiny_pct = (self.size_buckets['tiny']['count'] / self.total_objects * 100)
        large_pct = ((self.size_buckets['medium']['count'] + self.size_buckets['large']['count']) / self.total_objects * 100)
        
        if tiny_pct > 70:
            print("❌ NOT RECOMMENDED - Too many small objects (>70%)")
            print("   Small objects incur per-request costs that outweigh tiering benefits.")
        elif large_pct > 60:
            print("✅ EXCELLENT CANDIDATE - Majority are medium/large objects")
            print("   Intelligent-Tiering will optimize costs based on access patterns.")
        else:
            print("⚠️  MODERATE CANDIDATE - Mixed object sizes")
            print("   Consider filtering small objects or using lifecycle policies.")
        print("=" * 70)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python s3_tiering_analyzer.py <bucket-name> [prefix]")
        print("\nExamples:")
        print("  python s3_tiering_analyzer.py my-bucket")
        print("  python s3_tiering_analyzer.py my-bucket data/archive/")
        sys.exit(1)
    
    bucket_name = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else ''
    
    analyzer = S3TieringAnalyzer()
    analyzer.scan(bucket_name, prefix)
