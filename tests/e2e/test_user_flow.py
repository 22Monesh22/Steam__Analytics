import pytest
from app import create_app
from app.models import db, User

class TestUserFlow:
    def setup_method(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def teardown_method(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_complete_user_flow(self):
        # 1. User registration
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123',
            'confirm_password': 'SecurePass123',
            'first_name': 'New',
            'last_name': 'User',
            'terms': 'y'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Registration successful' in response.data or b'Login' in response.data
        
        # 2. User login
        response = self.client.post('/auth/login', data={
            'email': 'newuser@example.com',
            'password': 'SecurePass123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Dashboard' in response.data or b'Welcome' in response.data
        
        # 3. Access dashboard
        response = self.client.get('/dashboard')
        assert response.status_code == 200
        
        # 4. Access analytics
        response = self.client.get('/analytics')
        assert response.status_code == 200
        
        # 5. Generate AI insight
        response = self.client.post('/ai/generate-insight', 
                                  json={'type': 'trend'},
                                  follow_redirects=True)
        # This might return an error if AI is not configured, but should not crash
        assert response.status_code == 200
        
        # 6. User logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data or b'Signed out' in response.data