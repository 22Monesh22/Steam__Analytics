 
class Recommendation:
    def __init__(self, user_id, game_id, is_recommended, hours_played, date):
        self.user_id = user_id
        self.game_id = game_id
        self.is_recommended = bool(is_recommended)
        self.hours_played = float(hours_played) if hours_played else 0.0
        self.date = date
    
    @classmethod
    def from_csv_row(cls, row):
        return cls(
            user_id=row['user_id'],
            game_id=row['game_id'],
            is_recommended=row['is_recommended'],
            hours_played=row.get('hours_played', 0),
            date=row.get('date', '')
        )
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'game_id': self.game_id,
            'is_recommended': self.is_recommended,
            'hours_played': self.hours_played,
            'date': str(self.date)
        }