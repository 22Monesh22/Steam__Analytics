# find_json.py
import os

def find_json_files():
    print("🔍 Searching for JSON files...")
    print("Current directory:", os.getcwd())
    print("\n")
    
    # Search in current directory and parent directory
    search_paths = [
        ".",  # Current directory
        "..", # Parent directory
        "../.." # Grandparent directory
    ]
    
    json_files_found = []
    
    for path in search_paths:
        print(f"📁 Searching in: {os.path.abspath(path)}")
        try:
            for file in os.listdir(path):
                if file.endswith('.json'):
                    full_path = os.path.join(path, file)
                    json_files_found.append(full_path)
                    print(f"   ✅ Found: {file}")
                    
                    # Show file size
                    file_size = os.path.getsize(full_path)
                    print(f"       Size: {file_size} bytes")
                    
                    # Try to read first few lines
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            first_line = f.readline().strip()
                            print(f"       First line: {first_line[:100]}...")
                    except:
                        print(f"       Could not read file content")
                        
        except Exception as e:
            print(f"   ❌ Could not search {path}: {e}")
    
    print("\n" + "="*60)
    
    if json_files_found:
        print(f"🎯 Found {len(json_files_found)} JSON file(s):")
        for file in json_files_found:
            print(f"   📄 {file}")
    else:
        print("❌ No JSON files found in searched locations")
        print("\n💡 Please create a JSON file or check the file name.")
    
    return json_files_found

if __name__ == "__main__":
    find_json_files()