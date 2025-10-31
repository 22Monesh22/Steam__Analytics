from app import create_app, db

app = create_app()

with app.app_context():
    # Check what tables exist
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print("Existing tables in database:")
    for table in tables:
        print(f"  - {table}")
    
    # Check the structure of user-related tables
    user_tables = [t for t in tables if 'user' in t.lower()]
    if user_tables:
        print("\nUser-related tables found:")
        for table in user_tables:
            columns = inspector.get_columns(table)
            print(f"  {table} columns:")
            for col in columns:
                print(f"    - {col['name']}: {col['type']}")
    else:
        print("\nNo user-related tables found!")