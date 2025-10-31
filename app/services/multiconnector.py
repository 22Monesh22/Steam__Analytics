import pandas as pd
import os
import json
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class MultiCSVConnector:
    def __init__(self, csv_config: Dict = None):
        self.csv_config = csv_config or {
            'games': 'data/raw/games.csv',
            'users': 'data/raw/users.csv', 
            'reviews': 'data/raw/recommendations.csv'
        }
        self.dataframes = {}
        self.load_all_data()
    
    def load_all_data(self):
        """Load all three CSV files"""
        for data_type, file_path in self.csv_config.items():
            try:
                if os.path.exists(file_path):
                    self.dataframes[data_type] = pd.read_csv(file_path)
                    logger.info(f"✅ Loaded {len(self.dataframes[data_type])} rows from {data_type}.csv")
                else:
                    logger.warning(f"⚠️ File not found: {file_path}")
                    self.dataframes[data_type] = pd.DataFrame()
            except Exception as e:
                logger.error(f"❌ Error loading {file_path}: {e}")
                self.dataframes[data_type] = pd.DataFrame()
    
    def get_user_recommendations(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Get personalized game recommendations for a user"""
        try:
            # If we have users and reviews data, use collaborative filtering
            if 'users' in self.dataframes and 'reviews' in self.dataframes:
                user_reviews = self.dataframes['reviews'][self.dataframes['reviews']['user_id'] == user_id]
                
                if not user_reviews.empty:
                    # Get user's preferred genres from their reviewed games
                    user_game_ids = user_reviews['app_id'].tolist()
                    user_games = self.dataframes['games'][self.dataframes['games']['app_id'].isin(user_game_ids)]
                    
                    if not user_games.empty:
                        preferred_genres = self.extract_genres(user_games)
                        return self.recommend_by_genres(preferred_genres, limit, exclude_games=user_game_ids)
            
            # Fallback: popular games if no user data
            return self.get_popular_games(limit)
            
        except Exception as e:
            logger.error(f"Error getting recommendations for user {user_id}: {e}")
            return self.get_popular_games(limit)
    
    def extract_genres(self, games_df: pd.DataFrame) -> List[str]:
        """Extract genres from games dataframe"""
        try:
            if 'genres' in games_df.columns:
                all_genres = []
                for genres in games_df['genres'].dropna():
                    if isinstance(genres, str):
                        # Handle both comma-separated and list formats
                        if ',' in genres:
                            all_genres.extend([g.strip() for g in genres.split(',')])
                        else:
                            all_genres.append(genres.strip())
                from collections import Counter
                return [genre for genre, count in Counter(all_genres).most_common(5)]
        except Exception as e:
            logger.error(f"Error extracting genres: {e}")
        return ['Action', 'Adventure']  # Default fallback
    
    def recommend_by_genres(self, genres: List[str], limit: int = 5, exclude_games: List = None) -> List[Dict]:
        """Recommend games based on genres"""
        try:
            exclude_games = exclude_games or []
            recommendations = []
            
            for genre in genres:
                genre_games = self.dataframes['games'][
                    (self.dataframes['games']['genres'].str.contains(genre, na=False)) &
                    (~self.dataframes['games']['app_id'].isin(exclude_games))
                ]
                
                # Sort by rating or popularity if available
                sort_column = 'rating' if 'rating' in genre_games.columns else 'positive_ratings' if 'positive_ratings' in genre_games.columns else None
                if sort_column and sort_column in genre_games.columns:
                    genre_games = genre_games.sort_values(sort_column, ascending=False)
                
                for _, game in genre_games.head(limit).iterrows():
                    recommendations.append({
                        'app_id': game.get('app_id'),
                        'name': game.get('name', 'Unknown Game'),
                        'genres': game.get('genres', ''),
                        'reason': f"Similar to your interest in {genre}",
                        'confidence': 'high' if genre == genres[0] else 'medium'
                    })
            
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error in genre-based recommendations: {e}")
            return self.get_popular_games(limit)
    
    def get_popular_games(self, limit: int = 10) -> List[Dict]:
        """Get most popular games"""
        try:
            games_df = self.dataframes.get('games')
            if games_df is None or games_df.empty:
                return []
            
            # Try different popularity metrics
            popularity_columns = ['positive_ratings', 'rating', 'recommendations']
            sort_column = None
            
            for col in popularity_columns:
                if col in games_df.columns:
                    sort_column = col
                    break
            
            if sort_column:
                popular_games = games_df.sort_values(sort_column, ascending=False).head(limit)
            else:
                popular_games = games_df.head(limit)
            
            return [
                {
                    'app_id': row.get('app_id'),
                    'name': row.get('name', 'Unknown Game'),
                    'genres': row.get('genres', ''),
                    'reason': 'Popular among players',
                    'confidence': 'high'
                }
                for _, row in popular_games.iterrows()
            ]
            
        except Exception as e:
            logger.error(f"Error getting popular games: {e}")
            return []
    
    def get_user_play_history(self, user_id: str) -> Dict:
        """Get user's play history and preferences"""
        try:
            user_data = {}
            
            # Get user info
            if 'users' in self.dataframes:
                user_info = self.dataframes['users'][self.dataframes['users']['user_id'] == user_id]
                if not user_info.empty:
                    user_data['user_info'] = user_info.iloc[0].to_dict()
            
            # Get user reviews
            if 'reviews' in self.dataframes:
                user_reviews = self.dataframes['reviews'][self.dataframes['reviews']['user_id'] == user_id]
                user_data['review_count'] = len(user_reviews)
                user_data['average_rating'] = user_reviews['rating'].mean() if 'rating' in user_reviews.columns else None
            
            # Get played games
            if 'reviews' in self.dataframes and 'games' in self.dataframes:
                reviewed_games = self.dataframes['reviews'][self.dataframes['reviews']['user_id'] == user_id]['app_id'].tolist()
                played_games = self.dataframes['games'][self.dataframes['games']['app_id'].isin(reviewed_games)]
                user_data['played_games'] = [
                    {'name': row['name'], 'genres': row.get('genres', '')} 
                    for _, row in played_games.iterrows()
                ]
                user_data['preferred_genres'] = self.extract_genres(played_games)
            
            return user_data
            
        except Exception as e:
            logger.error(f"Error getting user history for {user_id}: {e}")
            return {}
    
    def search_games(self, query: str, limit: int = 10) -> List[Dict]:
        """Search games by name, genre, or description"""
        try:
            games_df = self.dataframes.get('games')
            if games_df is None or games_df.empty:
                return []
            
            query_lower = query.lower()
            results = []
            
            # Search in name
            name_matches = games_df[games_df['name'].str.contains(query_lower, na=False, case=False)]
            for _, game in name_matches.iterrows():
                results.append({
                    'app_id': game.get('app_id'),
                    'name': game.get('name'),
                    'genres': game.get('genres', ''),
                    'match_type': 'name',
                    'confidence': 'high'
                })
            
            # Search in genres
            genre_matches = games_df[games_df['genres'].str.contains(query_lower, na=False, case=False)]
            for _, game in genre_matches.iterrows():
                results.append({
                    'app_id': game.get('app_id'),
                    'name': game.get('name'),
                    'genres': game.get('genres', ''),
                    'match_type': 'genre',
                    'confidence': 'medium'
                })
            
            # Search in description if available
            if 'description' in games_df.columns:
                desc_matches = games_df[games_df['description'].str.contains(query_lower, na=False, case=False)]
                for _, game in desc_matches.iterrows():
                    results.append({
                        'app_id': game.get('app_id'),
                        'name': game.get('name'),
                        'genres': game.get('genres', ''),
                        'match_type': 'description',
                        'confidence': 'low'
                    })
            
            # Remove duplicates and return
            seen = set()
            unique_results = []
            for result in results:
                identifier = result['app_id']
                if identifier not in seen:
                    seen.add(identifier)
                    unique_results.append(result)
            
            return unique_results[:limit]
            
        except Exception as e:
            logger.error(f"Error searching games: {e}")
            return []
    
    def get_game_details(self, app_id: str) -> Optional[Dict]:
        """Get detailed information about a specific game"""
        try:
            games_df = self.dataframes.get('games')
            if games_df is None:
                return None
            
            game = games_df[games_df['app_id'] == app_id]
            if game.empty:
                return None
            
            game_data = game.iloc[0].to_dict()
            
            # Add review data if available
            if 'reviews' in self.dataframes:
                game_reviews = self.dataframes['reviews'][self.dataframes['reviews']['app_id'] == app_id]
                game_data['review_count'] = len(game_reviews)
                game_data['average_rating'] = game_reviews['rating'].mean() if 'rating' in game_reviews.columns else None
                game_data['recent_reviews'] = game_reviews.head(5).to_dict('records')
            
            return game_data
            
        except Exception as e:
            logger.error(f"Error getting game details for {app_id}: {e}")
            return None
    
    def get_dataset_stats(self) -> Dict:
        """Get statistics about the entire dataset"""
        stats = {}
        
        try:
            # Games stats
            if 'games' in self.dataframes:
                games_df = self.dataframes['games']
                stats['total_games'] = len(games_df)
                stats['games_with_genres'] = games_df['genres'].notna().sum() if 'genres' in games_df.columns else 0
                if 'genres' in games_df.columns:
                    all_genres = self.extract_genres(games_df)
                    stats['top_genres'] = all_genres[:10]
            
            # Users stats
            if 'users' in self.dataframes:
                users_df = self.dataframes['users']
                stats['total_users'] = len(users_df)
            
            # Reviews stats
            if 'reviews' in self.dataframes:
                reviews_df = self.dataframes['reviews']
                stats['total_reviews'] = len(reviews_df)
                if 'rating' in reviews_df.columns:
                    stats['average_rating'] = reviews_df['rating'].mean()
            
        except Exception as e:
            logger.error(f"Error getting dataset stats: {e}")
        
        return stats