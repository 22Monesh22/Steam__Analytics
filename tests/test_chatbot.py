import os
import json
import google.generativeai as genai

def debug_test():
    GEMINI_API_KEY = "AIzaSyAcO-KsHDV8cRathRRUqyolzc3PkiPQPbE"
    META_JSON_PATH = "./project_metadata.json"
    
    print("🔍 Debug Test Starting...")
    
    # 1. Check if JSON file exists and is valid
    if not os.path.exists(META_JSON_PATH):
        print(f"❌ File not found: {META_JSON_PATH}")
        # Try different paths
        alternative_paths = [
            "project_metadata.json",
            "../project_metadata.json",
            "./tests/project_metadata.json"
        ]
        for path in alternative_paths:
            if os.path.exists(path):
                META_JSON_PATH = path
                print(f"✅ Found file at: {path}")
                break
        else:
            print("❌ No JSON file found in common locations")
            return
    
    # 2. Test JSON loading
    try:
        with open(META_JSON_PATH, 'r', encoding='utf-8') as f:
            meta_data = json.load(f)
        print(f"✅ JSON loaded successfully: {meta_data.get('project_name', 'Unknown')}")
    except Exception as e:
        print(f"❌ JSON loading failed: {e}")
        return
    
    # 3. Test Gemini API
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        test_response = model.generate_content("Say 'Hello World'")
        print(f"✅ Gemini API working: {test_response.text}")
    except Exception as e:
        print(f"❌ Gemini API failed: {e}")
        return
    
    print("🎉 All basic tests passed!")

if __name__ == "__main__":
    debug_test()