import requests
import json
import ssl
import urllib3
from urllib3.poolmanager import PoolManager

# Disable SSL verification (for development only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context
        )

def ask_deepseek(question, api_key="your-deepseek-api-key"):
    url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": question}],
        "stream": False,
        "temperature": 0.7
    }
    
    try:
        # Create session with SSL context that doesn't verify certificates
        session = requests.Session()
        
        # Create SSL context that doesn't verify
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Mount adapter for both http and https
        adapter = CustomHttpAdapter(ssl_context=ssl_context)
        session.mount("https://", adapter)
        
        response = session.post(url, headers=headers, json=data, timeout=30, verify=False)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"AI Service temporarily unavailable. Error: {str(e)}"