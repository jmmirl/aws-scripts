#!/usr/bin/env python3
import sys
import os
import signal
from datetime import datetime

class LocalTieringAnalyzer:
    def __init__(self):
        self.total_files = 0
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
    
    def _categorize_file(self, size):
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
    
    def scan(self, directory):
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist")
            sys.exit(1)
        
        if not os.path.isdir(directory):
            print(f"Error: '{directory}' is not a directory")
            sys.exit(1)
        
        print(f"🔍 Scanning: {directory}\n")
        start_time = datetime.now()
        
        for root, dirs, files in os.walk(directory):
            if self.interrupted:
                break
            
            for filename in files:
                if self.interrupted:
                    break
                
                filepath = os.path.join(root, filename)
                try:
                    size = os.path.getsize(filepath)
                    self.total_files += 1
                    self.total_size += size
                    self._categorize_file(size)
                    
                    print(f"\r📄 Files: {self.total_files:,} | Size: {self._format_size(self.total_size)} | Current: {filename[:50]}", end='', flush=True)
                except (OSError, PermissionError):
                    continue
        
        print("\n")
        elapsed = (datetime.now() - start_time).total_seconds()
        self._print_summary(elapsed)
    
    def _print_summary(self, elapsed):
        print("=" * 70)
        print("📊 S3 INTELLIGENT-TIERING ANALYSIS")
        print("=" * 70)
        print(f"Total Files: {self.total_files:,}")
        print(f"Total Size: {self._format_size(self.total_size)}")
        print(f"Scan Time: {elapsed:.2f}s\n")
        
        print("File Size Distribution:")
        print("-" * 70)
        for name, info in self.size_buckets.items():
            pct = (info['count'] / self.total_files * 100) if self.total_files > 0 else 0
            print(f"  {name.capitalize():8} | {info['count']:8,} files ({pct:5.1f}%) | {self._format_size(info['size'])}")
        
        print("\n" + "=" * 70)
        print("💡 RECOMMENDATION")
        print("=" * 70)
        
        if self.total_files == 0:
            print("⚠️  NO FILES FOUND")
            print("=" * 70)
            return
        
        tiny_pct = (self.size_buckets['tiny']['count'] / self.total_files * 100)
        large_pct = ((self.size_buckets['medium']['count'] + self.size_buckets['large']['count']) / self.total_files * 100)
        
        if tiny_pct > 70:
            print("❌ NOT RECOMMENDED - Too many small files (>70%)")
            print("   Small objects incur per-request costs that outweigh tiering benefits.")
        elif large_pct > 60:
            print("✅ EXCELLENT CANDIDATE - Majority are medium/large files")
            print("   Intelligent-Tiering will optimize costs based on access patterns.")
        else:
            print("⚠️  MODERATE CANDIDATE - Mixed file sizes")
            print("   Consider filtering small objects or using lifecycle policies.")
        print("=" * 70)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 local_tiering_analyzer.py <directory_path>")
        print("\nExample:")
        print("  python3 local_tiering_analyzer.py /path/to/your/data")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    analyzer = LocalTieringAnalyzer()
    analyzer.scan(directory)
