import pytest
from app.models import User, Game, Insight

@pytest.fixture
def sample_user():
    """Create a sample user for testing"""
    user = User(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    user.set_password('testpassword')
    return user

@pytest.fixture
def sample_game():
    """Create a sample game for testing"""
    game = Game(
        steam_appid=12345,
        name='Test Game',
        developer='Test Developer',
        publisher='Test Publisher',
        price=29.99,
        rating=4.5,
        positive_ratings=1000,
        negative_ratings=100,
        genres='Action, Adventure',
        categories='Single-player, Multiplayer'
    )
    return game

@pytest.fixture
def sample_insight():
    """Create a sample AI insight for testing"""
    insight = Insight(
        user_id=1,
        title='Test Insight',
        content='This is a test insight generated for testing purposes.',
        insight_type='trend',
        is_public=True
    )
    return insight

@pytest.fixture
def multiple_games():
    """Create multiple sample games for testing"""
    games = [
        Game(
            steam_appid=i,
            name=f'Test Game {i}',
            developer=f'Developer {i}',
            price=9.99 + i,
            rating=3.0 + (i * 0.1),
            positive_ratings=100 * i,
            negative_ratings=10 * i
        )
        for i in range(1, 6)
    ]
    return games