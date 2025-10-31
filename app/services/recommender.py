import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from app.models import db
from app.models.game import Game
import logging

class Recommender:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.similarity_matrix = None
        self.game_features = None
    
    def build_recommendation_model(self):
        """Build game recommendation model"""
        try:
            games = Game.query.all()
            
            if not games:
                self.logger.warning("No games found for recommendation model")
                return False
            
            # Prepare features for similarity calculation
            game_data = []
            for game in games:
                features = f"{game.genres or ''} {game.categories or ''} {game.tags or ''}"
                game_data.append({
                    'id': game.id,
                    'name': game.name,
                    'features': features,
                    'rating': game.rating or 0,
                    'price': game.price or 0
                })
            
            # Create TF-IDF matrix for text features
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = vectorizer.fit_transform([g['features'] for g in game_data])
            
            # Calculate similarity matrix
            self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
            self.game_features = game_data
            
            self.logger.info(f"Built recommendation model for {len(games)} games")
            return True
            
        except Exception as e:
            self.logger.error(f"Error building recommendation model: {e}")
            return False
    
    def get_similar_games(self, game_id, top_n=5):
        """Get similar games based on content"""
        if self.similarity_matrix is None:
            if not self.build_recommendation_model():
                return []
        
        try:
            # Find game index
            game_idx = None
            for idx, game in enumerate(self.game_features):
                if game['id'] == game_id:
                    game_idx = idx
                    break
            
            if game_idx is None:
                return []
            
            # Get similarity scores
            similarity_scores = list(enumerate(self.similarity_matrix[game_idx]))
            
            # Sort by similarity score
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            
            # Get top N similar games (excluding the game itself)
            similar_games = []
            for idx, score in similarity_scores[1:top_n+1]:
                similar_game = self.game_features[idx]
                similar_game['similarity_score'] = float(score)
                similar_games.append(similar_game)
            
            return similar_games
            
        except Exception as e:
            self.logger.error(f"Error getting similar games: {e}")
            return []
    
    def get_popular_recommendations(self, top_n=10):
        """Get popular game recommendations"""
        try:
            popular_games = Game.query.order_by(
                Game.total_recommendations.desc(),
                Game.rating.desc()
            ).limit(top_n).all()
            
            recommendations = []
            for game in popular_games:
                recommendations.append({
                    'id': game.id,
                    'name': game.name,
                    'developer': game.developer,
                    'rating': game.rating,
                    'price': game.price,
                    'recommendations': game.total_recommendations,
                    'reason': 'Highly rated and popular'
                })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error getting popular recommendations: {e}")
            return []
    
    def get_personalized_recommendations(self, user_preferences, top_n=5):
        """Get personalized recommendations based on user preferences"""
        try:
            # This would integrate with user data in a real application
            # For now, return popular recommendations
            return self.get_popular_recommendations(top_n)
            
        except Exception as e:
            self.logger.error(f"Error getting personalized recommendations: {e}")
            return []