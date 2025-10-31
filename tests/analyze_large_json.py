# analyze_large_json.py
import os
import json

def analyze_large_file():
    file_path = "project_metadata.json"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"📊 Analyzing large file: {file_path}")
    print("=" * 60)
    
    # Get file size
    file_size = os.path.getsize(file_path)
    print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
    
    # Count lines
    with open(file_path, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
    print(f"Total lines: {line_count:,}")
    
    # Read first few lines to understand structure
    print("\n🔍 First 5 lines:")
    print("-" * 40)
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                break
            print(f"Line {i+1}: {line.strip()[:100]}...")
    
    # Check if it's JSONL (JSON Lines)
    print("\n🔍 Checking if it's JSONL format...")
    valid_jsonl_count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 10:  # Check first 10 lines
                break
            line = line.strip()
            if line:  # Skip empty lines
                try:
                    json.loads(line)
                    valid_jsonl_count += 1
                    print(f"Line {i+1}: ✅ Valid JSON object")
                except:
                    print(f"Line {i+1}: ❌ Not valid JSON")
    
    if valid_jsonl_count > 0:
        print(f"\n✅ This appears to be a JSONL file with {valid_jsonl_count} valid JSON objects in first 10 lines")
    else:
        print("\n❌ This doesn't appear to be standard JSON or JSONL")

if __name__ == "__main__":
    analyze_large_file()