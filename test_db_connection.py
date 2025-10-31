from app import create_app, db

app = create_app()

with app.app_context():
    try:
        # Test database connection
        db.engine.connect()
        print("✅ Database connection successful!")
        
        # Test if we can query insights
        from app.models.insight import Insight
        insights_count = Insight.query.count()
        print(f"✅ Total insights in database: {insights_count}")
        
    except Exception as e:
        print(f"❌ Database error: {e}")