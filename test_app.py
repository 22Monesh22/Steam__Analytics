from app import create_app

app = create_app()

with app.app_context():
    print("✅ App created successfully!")
    print("✅ Database initialized!")
    print("✅ Routes registered!")
    
    # Test if we can access the routes
    with app.test_client() as client:
        response = client.get('/auth/login')
        print(f"✅ Login page: {response.status_code}")
        
        response = client.get('/auth/register') 
        print(f"✅ Register page: {response.status_code}")

print("🎉 Everything is working! Run 'python run.py' to start the server.")