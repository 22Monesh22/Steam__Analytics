from app import create_app, db
from app.models.user import User
from app.models.insight import Insight
from app.services.ai_engine import AIEngine
from app.services.simple_ai_engine import SimpleAIEngine

app = create_app()

with app.app_context():
    try:
        # Get a user
        user = User.query.first()
        if not user:
            print("❌ No users found in database")
            exit(1)
            
        print(f"✅ Using user: {user.username}")
        
        # Test 1: Try OpenAI engine
        print("\n1. Testing OpenAI Engine...")
        try:
            ai_engine = AIEngine()
            data_context = {"test": "data"}
            insight_text = ai_engine.generate_insight(data_context, "trend")
            print(f"✅ OpenAI insight: {insight_text}")
        except Exception as e:
            print(f"❌ OpenAI failed: {e}")
        
        # Test 2: Try Simple AI engine
        print("\n2. Testing Simple AI Engine...")
        try:
            simple_engine = SimpleAIEngine()
            insight_text = simple_engine.generate_insight({}, "trend")
            print(f"✅ Simple AI insight: {insight_text}")
        except Exception as e:
            print(f"❌ Simple AI failed: {e}")
            
        # Test 3: Save an insight to database
        print("\n3. Testing Database Save...")
        try:
            insight = Insight(
                user_id=user.id,
                title="AI Trend Analysis",
                content="Sample AI-generated insight about gaming trends.",
                insight_type="trend"
            )
            db.session.add(insight)
            db.session.commit()
            print(f"✅ Insight saved with ID: {insight.id}")
        except Exception as e:
            print(f"❌ Database save failed: {e}")
            db.session.rollback()
            
    except Exception as e:
        print(f"❌ Overall error: {e}")
        import traceback
        traceback.print_exc()