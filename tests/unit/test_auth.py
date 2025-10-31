import pytest
from app import create_app
from app.models import db, User
from auth.utils import password_strength_check, generate_jwt_token

class TestAuth:
    def setup_method(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def teardown_method(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_password_strength(self):
        # Test weak password
        is_strong, message = password_strength_check('weak')
        assert not is_strong
        assert 'at least 8 characters' in message
        
        # Test strong password
        is_strong, message = password_strength_check('StrongPass123')
        assert is_strong
        assert 'strong' in message
    
    def test_user_registration(self):
        response = self.client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'confirm_password': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'User'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should redirect to login page after successful registration
    
    def test_user_login(self):
        # First create a user
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('TestPass123')
        
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        
        # Test login
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'TestPass123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_jwt_token_generation(self):
        with self.app.app_context():
            token = generate_jwt_token(1)
            assert token is not None
            assert isinstance(token, str)