# Add this to your analytics_bp.py or create a new test file
import pandas as pd
import os

def debug_csv_structure():
    """Debug function to check your actual CSV structure"""
    base_path = 'raw'
    
    print("🔍 DEBUGGING CSV STRUCTURE")
    print("=" * 50)
    
    # Check games.csv
    games_path = os.path.join(base_path, 'games.csv')
    if os.path.exists(games_path):
        games_df = pd.read_csv(games_path)
        print(f"📊 GAMES.CSV - {len(games_df)} rows")
        print("Columns:", list(games_df.columns))
        if len(games_df) > 0:
            print("First row sample:")
            for col, val in games_df.iloc[0].items():
                print(f"  {col}: {val}")
        print()
    
    # Check users.csv  
    users_path = os.path.join(base_path, 'users.csv')
    if os.path.exists(users_path):
        users_df = pd.read_csv(users_path)
        print(f"👥 USERS.CSV - {len(users_df)} rows")
        print("Columns:", list(users_df.columns))
        if len(users_df) > 0:
            print("First row sample:")
            for col, val in users_df.iloc[0].items():
                print(f"  {col}: {val}")
        print()
    
    # Check recommendations.csv
    recs_path = os.path.join(base_path, 'recommendations.csv')
    if os.path.exists(recs_path):
        recs_df = pd.read_csv(recs_path)
        print(f"💡 RECOMMENDATIONS.CSV - {len(recs_df)} rows")
        print("Columns:", list(recs_df.columns))
        if len(recs_df) > 0:
            print("First row sample:")
            for col, val in recs_df.iloc[0].items():
                print(f"  {col}: {val}")

# Run this function to see your actual CSV structure
debug_csv_structure()