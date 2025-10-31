from app import create_app, db

app = create_app()

with app.app_context():
    try:
        print("Testing final configuration...")
        
        # Test database
        db.engine.connect()
        print("✅ Database connection successful!")
        
        # Test models
        from app.models.insight import Insight
        insights_count = Insight.query.count()
        print(f"✅ Insights count: {insights_count}")
        
        from app.models.user import User
        users_count = User.query.count()
        print(f"✅ Users count: {users_count}")
        
        print("🎉 All tests passed! Your app should work now.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()