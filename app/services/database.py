import pandas as pd
from app.models import db
from app.models.game import Game
from app.models.user import User
import logging

class DatabaseManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def import_games_data(self, csv_path):
        """Import games data from CSV"""
        try:
            df = pd.read_csv(csv_path)
            games_imported = 0
            
            for _, row in df.iterrows():
                game = Game(
                    steam_appid=row.get('steam_appid'),
                    name=row.get('name'),
                    developer=row.get('developer'),
                    publisher=row.get('publisher'),
                    release_date=pd.to_datetime(row.get('release_date', '1900-01-01')),
                    price=row.get('price', 0.0),
                    rating=row.get('rating', 0.0),
                    positive_ratings=row.get('positive_ratings', 0),
                    negative_ratings=row.get('negative_ratings', 0),
                    owners=row.get('owners', '0-0'),
                    average_playtime=row.get('average_playtime', 0),
                    median_playtime=row.get('median_playtime', 0),
                    genres=row.get('genres', ''),
                    categories=row.get('categories', ''),
                    tags=row.get('tags', '')
                )
                
                db.session.add(game)
                games_imported += 1
            
            db.session.commit()
            self.logger.info(f"Imported {games_imported} games from {csv_path}")
            return games_imported
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error importing games data: {e}")
            return 0
    
    def export_analytics_data(self, format='csv'):
        """Export analytics data"""
        try:
            games = Game.query.all()
            games_data = []
            
            for game in games:
                games_data.append({
                    'name': game.name,
                    'developer': game.developer,
                    'rating': game.rating,
                    'price': game.price,
                    'recommendations': game.total_recommendations,
                    'release_date': game.release_date
                })
            
            df = pd.DataFrame(games_data)
            
            if format == 'csv':
                return df.to_csv(index=False)
            elif format == 'json':
                return df.to_json(orient='records', indent=2)
            else:
                return df.to_string()
                
        except Exception as e:
            self.logger.error(f"Error exporting data: {e}")
            return None
    
    def get_database_stats(self):
        """Get database statistics"""
        try:
            stats = {
                'total_games': Game.query.count(),
                'total_users': User.query.count(),
                'database_size': 'N/A',  # Would require specific database queries
                'last_updated': 'N/A'
            }
            return stats
        except Exception as e:
            self.logger.error(f"Error getting database stats: {e}")
            return {}