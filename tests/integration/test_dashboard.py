import pytest
from app import create_app
from app.models import db, User
from flask_login import login_user

class TestDashboard:
    def setup_method(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create test user
            user = User(
                username='testuser',
                email='test@example.com',
                first_name='Test',
                last_name='User'
            )
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id
    
    def teardown_method(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_dashboard_access_authenticated(self):
        with self.app.app_context():
            user = User.query.get(self.user_id)
            
            with self.client:
                # Login user
                login_user(user)
                
                # Access dashboard
                response = self.client.get('/dashboard')
                assert response.status_code == 200
                assert b'Dashboard' in response.data
    
    def test_dashboard_access_unauthenticated(self):
        response = self.client.get('/dashboard', follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to login page
        assert b'Login' in response.data or b'Sign in' in response.data
    
    def test_dashboard_api_endpoints(self):
        with self.app.app_context():
            user = User.query.get(self.user_id)
            
            with self.client:
                login_user(user)
                
                # Test metrics endpoint
                response = self.client.get('/api/metrics')
                assert response.status_code == 200
                data = response.get_json()
                assert 'total_games' in data
                
                # Test popular games endpoint
                response = self.client.get('/api/popular-games')
                assert response.status_code == 200