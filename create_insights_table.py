from app import create_app, db
from app.models.insight import Insight

app = create_app()

with app.app_context():
    try:
        # Create only the insights table
        Insight.__table__.create(db.engine)
        print("✅ Insights table created successfully!")
    except Exception as e:
        print(f"Note: {e}")