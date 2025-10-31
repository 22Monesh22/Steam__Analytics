from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        print("🔄 Resetting database with insights...")
        
        # Disable foreign key checks
        db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))
        db.session.commit()
        print("✅ Foreign key checks disabled")
        
        # Drop all tables
        db.drop_all()
        print("✅ Dropped all tables")
        
        # Re-enable foreign key checks
        db.session.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))
        db.session.commit()
        print("✅ Foreign key checks enabled")
        
        # Import models
        from app.models.user import User
        from app.models.insight import Insight
        
        # Create tables
        db.create_all()
        print("✅ Created all tables")
        
        # Create a test user
        from app import bcrypt
        
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(
            username='admin',
            email='admin@steamanalytics.com',
            password_hash=hashed_password,
            first_name='Admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Created admin user")
        
        # Create a sample insight
        sample_insight = Insight(
            user_id=admin_user.id,
            title='Popular Game Trends',
            content='Analysis shows that strategy games are trending among users aged 25-35.',
            insight_type='trend',
            data_context='{"age_group": "25-35", "genre": "strategy"}',
            confidence_score=0.85,
            is_public=True,
            tags='trend,strategy,demographics'
        )
        db.session.add(sample_insight)
        db.session.commit()
        print("✅ Created sample insight")
        
        print("   Username: admin")
        print("   Password: admin123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()