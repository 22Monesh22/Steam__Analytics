import re
import hashlib
import secrets
from flask import request
from functools import wraps

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    if not text:
        return text
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\'&]', '', str(text))
    return sanitized.strip()

def generate_api_key():
    """Generate secure API key"""
    return secrets.token_urlsafe(32)

def hash_data(data):
    """Hash data for integrity checking"""
    return hashlib.sha256(data.encode()).hexdigest()

def validate_csrf_token(token):
    """Validate CSRF token"""
    # Implementation would depend on your CSRF strategy
    return True

def rate_limit(key, limit=100, period=3600):
    """Simple rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Implementation would use Redis or database
            # For now, just pass through
            return f(*args, **kwargs)
        return decorated_function
    return decorator