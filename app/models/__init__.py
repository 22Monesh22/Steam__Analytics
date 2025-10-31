from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

# Import all models
from app.models.user import User
from app.models.game import Game
from app.models.insight import Insight
from app.models.session import UserSession

__all__ = ['User', 'Game', 'Insight', 'UserSession', 'db', 'bcrypt']