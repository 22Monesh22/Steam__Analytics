import pandas as pd
import numpy as np
from app.models import db
from app.models.game import Game
from app.models.user import User
from datetime import datetime, timedelta
import logging

class BIAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_overview_metrics(self):
        """Get key metrics for dashboard overview"""
        try:
            total_games = Game.query.count()
            total_users = User.query.count()
            
            # Calculate total recommendations
            total_recommendations = db.session.query(
                db.func.sum(Game.total_recommendations)
            ).scalar() or 0
            
            # Calculate average rating
            avg_rating = db.session.query(
                db.func.avg(Game.rating)
            ).scalar() or 0
            
            return {
                'total_games': total_games,
                'total_users': total_users,
                'total_recommendations': int(total_recommendations),
                'avg_rating': round(avg_rating, 2)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting overview metrics: {e}")
            return {}
    
    def get_popular_games_data(self, limit=10):
        """Get data for popular games chart"""
        try:
            games = Game.query.order_by(Game.total_recommendations.desc()).limit(limit).all()
            
            game_data = []
            for game in games:
                game_data.append({
                    'name': game.name,
                    'recommendations': game.total_recommendations or 0,
                    'rating': game.rating or 0,
                    'price': game.price or 0,
                    'developer': game.developer or 'Unknown'
                })
            
            return game_data
            
        except Exception as e:
            self.logger.error(f"Error getting popular games data: {e}")
            return []
    
    def get_genre_analysis(self):
        """Analyze game genres and their performance"""
        try:
            # This would typically query your games data
            # For now, return sample data
            return {
                'action': 1250,
                'adventure': 890,
                'strategy': 760,
                'rpg': 680,
                'simulation': 540,
                'sports': 320
            }
            
        except Exception as e:
            self.logger.error(f"Error in genre analysis: {e}")
            return {}
    
    def get_user_behavior_insights(self):
        """Analyze user behavior patterns"""
        try:
            # Sample user behavior insights
            return {
                'avg_playtime': 45.2,
                'completion_rate': 0.68,
                'preferred_genres': ['Action', 'Adventure', 'RPG'],
                'peak_hours': [18, 19, 20, 21],  # 6 PM - 9 PM
                'retention_rate': 0.72
            }
            
        except Exception as e:
            self.logger.error(f"Error in user behavior analysis: {e}")
            return {}
    
    def get_trend_analysis(self, days=30):
        """Analyze trends over time"""
        try:
            # This would typically query time-series data
            # For now, return sample trend data
            dates = pd.date_range(end=datetime.now(), periods=days).tolist()
            trends = {
                'dates': [d.strftime('%Y-%m-%d') for d in dates],
                'recommendations': np.random.randint(100, 1000, days).tolist(),
                'new_users': np.random.randint(10, 100, days).tolist(),
                'avg_ratings': np.random.uniform(3.5, 4.8, days).tolist()
            }
            
            return trends
            
        except Exception as e:
            self.logger.error(f"Error in trend analysis: {e}")
            return {}