import redis
import json
import pickle
from datetime import timedelta
import logging

class CacheService:
    def __init__(self, redis_url='redis://localhost:6379/0'):
        try:
            self.redis_client = redis.from_url(redis_url)
            self.logger = logging.getLogger(__name__)
        except Exception as e:
            self.redis_client = None
            self.logger.error(f"Redis connection failed: {e}")
    
    def set(self, key, value, expire=3600):
        """Set cache value"""
        if not self.redis_client:
            return False
        
        try:
            serialized_value = pickle.dumps(value)
            self.redis_client.setex(key, timedelta(seconds=expire), serialized_value)
            return True
        except Exception as e:
            self.logger.error(f"Cache set error: {e}")
            return False
    
    def get(self, key):
        """Get cache value"""
        if not self.redis_client:
            return None
        
        try:
            serialized_value = self.redis_client.get(key)
            if serialized_value:
                return pickle.loads(serialized_value)
            return None
        except Exception as e:
            self.logger.error(f"Cache get error: {e}")
            return None
    
    def delete(self, key):
        """Delete cache key"""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            self.logger.error(f"Cache delete error: {e}")
            return False
    
    def clear_pattern(self, pattern):
        """Clear keys matching pattern"""
        if not self.redis_client:
            return False
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception as e:
            self.logger.error(f"Cache clear pattern error: {e}")
            return False
    
    def get_stats(self):
        """Get cache statistics"""
        if not self.redis_client:
            return {'status': 'disabled'}
        
        try:
            info = self.redis_client.info()
            return {
                'status': 'connected',
                'used_memory': info.get('used_memory_human', 'N/A'),
                'connected_clients': info.get('connected_clients', 0),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0)
            }
        except Exception as e:
            self.logger.error(f"Cache stats error: {e}")
            return {'status': 'error', 'error': str(e)}