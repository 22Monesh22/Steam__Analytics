import os

print("🔍 Steam Analytics - Debug Information")
print("=" * 50)

print(f"Current directory: {os.getcwd()}")
print(f"Templates folder exists: {os.path.exists('templates')}")
print(f"Index.html exists: {os.path.exists('templates/index.html')}")

if os.path.exists('templates'):
    print("Templates folder contents:")
    for item in os.listdir('templates'):
        print(f"  - {item}")

print(f"App folder exists: {os.path.exists('app')}")
if os.path.exists('app'):
    print("App folder contents:")
    for item in os.listdir('app'):
        print(f"  - {item}")

# Test Flask template loading
from flask import Flask
app = Flask(__name__)
print(f"Default template folder: {app.template_folder}")

# Test with explicit path
app2 = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
print(f"Custom template folder: {app2.template_folder}")
print(f"Custom template folder exists: {os.path.exists(app2.template_folder)}")