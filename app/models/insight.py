from app import db  # Correct import
from datetime import datetime

class Insight(db.Model):
    __tablename__ = 'insights'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    insight_type = db.Column(db.String(50), nullable=False)  # trend, user_behavior, genre, etc.
    data_context = db.Column(db.Text)  # JSON string of data used for generation
    confidence_score = db.Column(db.Float, default=0.0)
    is_public = db.Column(db.Boolean, default=False)
    tags = db.Column(db.Text)  # Comma-separated tags
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Add relationship to User
    user = db.relationship('User', backref=db.backref('insights', lazy=True))
    
    def __repr__(self):
        return f'<Insight {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'type': self.insight_type,
            'created_at': self.created_at.isoformat(),
            'tags': self.tags.split(',') if self.tags else []
        }