from app import create_app, db
from app.models.user import User
from app.models.insight import Insight

app = create_app()

with app.app_context():
    try:
        # Get or create a test user
        user = User.query.filter_by(username="demo").first()
        if not user:
            print("❌ No demo user found. Please login and create a user first.")
        else:
            print(f"✅ Found user: {user.username} (ID: {user.id})")
            
            # Test saving an insight
            test_insight = Insight(
                user_id=user.id,
                title="Test Insight",
                content="This is a test insight to verify database functionality.",
                insight_type="test"
            )
            
            db.session.add(test_insight)
            db.session.commit()
            
            print("✅ Insight saved successfully!")
            print(f"Insight ID: {test_insight.id}")
            
            # Verify we can retrieve it
            saved_insight = Insight.query.get(test_insight.id)
            print(f"✅ Retrieved insight: {saved_insight.title}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()