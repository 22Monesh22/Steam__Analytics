 
import json
from datetime import datetime

def format_number(num):
    """Format numbers for display"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num)

def safe_json_loads(data, default=None):
    """Safely parse JSON data"""
    if default is None:
        default = {}
    try:
        return json.loads(data)
    except:
        return default

def get_current_time():
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")