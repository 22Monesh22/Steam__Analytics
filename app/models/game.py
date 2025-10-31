from app.models import db
from datetime import datetime

class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    steam_appid = db.Column(db.Integer, unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    developer = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    release_date = db.Column(db.Date)
    price = db.Column(db.Float, default=0.0)
    rating = db.Column(db.Float)
    positive_ratings = db.Column(db.Integer, default=0)
    negative_ratings = db.Column(db.Integer, default=0)
    owners = db.Column(db.String(100))
    average_playtime = db.Column(db.Integer, default=0)
    median_playtime = db.Column(db.Integer, default=0)
    genres = db.Column(db.Text)
    categories = db.Column(db.Text)
    tags = db.Column(db.Text)
    
    # Analytics fields
    total_recommendations = db.Column(db.Integer, default=0)
    recommendation_score = db.Column(db.Float, default=0.0)
    popularity_rank = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Game {self.name}>'
    
    def calculate_recommendation_score(self):
        if self.positive_ratings + self.negative_ratings > 0:
            return (self.positive_ratings / (self.positive_ratings + self.negative_ratings)) * 100
        return 0.0