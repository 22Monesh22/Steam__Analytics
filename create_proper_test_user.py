from app import create_app, db, bcrypt
from app.models.user import User
from app.models.insight import Insight

app = create_app()

with app.app_context():
    try:
        # Delete the existing test user if it exists
        existing_user = User.query.filter_by(username="testuser").first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
            print("Removed existing test user")
        
        # Check if demo user already exists
        demo_user = User.query.filter_by(username="demo").first()
        if demo_user:
            db.session.delete(demo_user)
            db.session.commit()
            print("Removed existing demo user")
        
        # Create new test user with properly hashed password
        demo_user = User(
            username="demo",
            email="demo@steamanalytics.com",
            first_name="Demo User",
            is_active=True
        )
        
        # Set password directly using bcrypt
        demo_user.password_hash = bcrypt.generate_password_hash("demo123").decode('utf-8')
        
        db.session.add(demo_user)
        db.session.commit()
        
        print("✅ Test user created successfully!")
        print(f"Username: demo")
        print(f"Password: demo123")
        print(f"User ID: {demo_user.id}")
        print(f"Email: {demo_user.email}")
        
        # Create a sample insight
        sample_insight = Insight(
            user_id=demo_user.id,
            title="Welcome to Steam Analytics",
            content="This platform analyzes 41 million+ Steam reviews to provide AI-powered insights for game developers and publishers.",
            insight_type="trend",
            tags="welcome,overview,analytics"
        )
        
        db.session.add(sample_insight)
        db.session.commit()
        
        print("✅ Sample insight created!")
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()