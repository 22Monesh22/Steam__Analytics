# check_json.py
import json
import os

def check_json_file(file_path):
    print(f"Checking JSON file: {file_path}")
    print("=" * 60)
    
    if not os.path.exists(file_path):
        print(f"❌ File does not exist: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print("File content:")
            print("-" * 40)
            print(content)
            print("-" * 40)
            print(f"File size: {len(content)} characters")
            
        # Try to parse JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("✅ JSON is valid!")
            print(f"JSON keys: {list(data.keys())}")
            return True
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")
        print(f"Error position: character {e.pos}")
        
        # Show context around the error
        if e.pos < len(content):
            start = max(0, e.pos - 20)
            end = min(len(content), e.pos + 20)
            error_context = content[start:end]
            print(f"Context around error: ...{error_context}...")
            
        # Check for common issues
        lines = content.split('\n')
        if len(lines) > 1:
            print(f"\nFirst few lines:")
            for i, line in enumerate(lines[:5], 1):
                print(f"Line {i}: {line}")
                
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

# Check your JSON file - replace with your actual file name
json_files_to_check = [
    "project_meta.json",
    "../project_meta.json",
    "your_project_meta.json"
]

for json_file in json_files_to_check:
    if os.path.exists(json_file):
        check_json_file(json_file)
        break
else:
    print("❌ No JSON file found. Please specify the correct file name.")