# process_steam_data_fixed.py
import json
import os
from collections import Counter

def clean_json_data(obj):
    """Recursively clean JSON data to remove non-serializable objects"""
    if isinstance(obj, dict):
        return {key: clean_json_data(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [clean_json_data(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    else:
        # Convert any other type to string
        return str(obj)

def process_steam_games():
    input_file = "project_metadata.json"
    output_file = "steam_chatbot_meta.json"
    
    print("🎮 Processing Steam Games Dataset...")
    print("=" * 60)
    
    games_data = []
    total_games = 0
    all_tags = []
    all_descriptions = []
    problematic_lines = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                game_data = json.loads(line)
                total_games += 1
                
                # Clean the data to remove any non-serializable objects
                cleaned_game_data = clean_json_data(game_data)
                games_data.append(cleaned_game_data)
                
                # Collect tags
                if 'tags' in cleaned_game_data and cleaned_game_data['tags']:
                    if isinstance(cleaned_game_data['tags'], list):
                        all_tags.extend(cleaned_game_data['tags'])
                
                # Collect descriptions for analysis
                if 'description' in cleaned_game_data and cleaned_game_data['description']:
                    all_descriptions.append(cleaned_game_data['description'])
                
                # Show progress
                if total_games % 10000 == 0:
                    print(f"📊 Processed {total_games:,} games...")
                
                # Sample first few games
                if total_games <= 3:
                    print(f"🎯 Game {total_games}:")
                    print(f"   App ID: {cleaned_game_data.get('app_id', 'N/A')}")
                    desc = cleaned_game_data.get('description', '')
                    print(f"   Description: {str(desc)[:100]}...")
                    print(f"   Tags: {cleaned_game_data.get('tags', [])[:5]}")
                    print()
                    
            except json.JSONDecodeError as e:
                problematic_lines.append((line_num, f"JSON Error: {e}"))
            except Exception as e:
                problematic_lines.append((line_num, f"Other Error: {e}"))
    
    print(f"\n📈 Dataset Summary:")
    print(f"   Total Games: {total_games:,}")
    print(f"   Total Tags: {len(all_tags):,}")
    print(f"   Unique Tags: {len(set(all_tags)):,}")
    print(f"   Games with Descriptions: {len(all_descriptions):,}")
    
    if problematic_lines:
        print(f"   Problematic Lines: {len(problematic_lines)}")
        for line_num, error in problematic_lines[:5]:  # Show first 5 errors
            print(f"      Line {line_num}: {error}")
    
    # Analyze most common tags
    tag_counter = Counter(all_tags)
    top_tags = tag_counter.most_common(20)
    
    print(f"\n🏷️ Top 20 Game Tags:")
    for tag, count in top_tags:
        print(f"   {tag}: {count} games")
    
    # Create comprehensive meta data for chatbot
    steam_meta = {
        "project_name": "Steam Games Analytics Platform",
        "version": "1.0.0",
        "description": "Advanced analytics platform for Steam games database with 50,000+ game records",
        "dataset_stats": {
            "total_games": total_games,
            "total_tags": len(all_tags),
            "unique_tags": len(set(all_tags)),
            "games_with_descriptions": len(all_descriptions),
            "file_size_mb": round(os.path.getsize(input_file) / 1024 / 1024, 2),
            "problematic_records": len(problematic_lines)
        },
        "top_tags": [{"tag": str(tag), "count": count} for tag, count in top_tags],  # Ensure tags are strings
        "sample_game_structure": {
            "app_id": "Steam application ID",
            "description": "Game description",
            "tags": ["Action", "Adventure", "RPG"]
        },
        "features": [
            "Game discovery and recommendation",
            "Tag-based game analysis",
            "Game description analysis",
            "Trend analysis across 50K+ games",
            "Genre popularity insights",
            "Game similarity matching"
        ],
        "supported_analyses": [
            "Game recommendation based on tags",
            "Genre popularity trends",
            "Game description sentiment analysis",
            "Tag correlation analysis",
            "Game discovery by features",
            "Market trend analysis"
        ],
        "data_sources": [
            "Steam Games Database (50,872 records)",
            "Game metadata and descriptions",
            "User-generated tags and categories"
        ],
        "report_types": [
            "Game recommendation reports",
            "Genre analysis dashboards",
            "Market trend reports",
            "Game discovery insights",
            "Tag popularity analysis"
        ]
    }
    
    # Clean the meta data before saving
    steam_meta_cleaned = clean_json_data(steam_meta)
    
    # Save the meta file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(steam_meta_cleaned, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Created steam_chatbot_meta.json")
        print(f"📁 Location: {os.path.abspath(output_file)}")
        
        # Verify the file can be loaded back
        with open(output_file, 'r', encoding='utf-8') as f:
            verified_data = json.load(f)
        print("✅ Meta file verification passed!")
        
    except Exception as e:
        print(f"❌ Error saving meta file: {e}")
        return
    
    # Save a sample of games for reference
    try:
        sample_games = games_data[:10]  # First 10 games
        with open('sample_steam_games.json', 'w', encoding='utf-8') as f:
            json.dump(sample_games, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Sample games saved to: sample_steam_games.json")
        
    except Exception as e:
        print(f"❌ Error saving sample games: {e}")
    
    return steam_meta_cleaned

if __name__ == "__main__":
    process_steam_games()