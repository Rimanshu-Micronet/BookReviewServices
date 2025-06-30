import redis
import json
import logging
from typing import Optional, Any
from config import settings

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Caching disabled.")
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Get data from cache"""
        if not self.redis_client:
            return None
        
        try:
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Set data in cache"""
        if not self.redis_client:
            return
        
        try:
            ttl = ttl or settings.cache_ttl
            self.redis_client.setex(key, ttl, json.dumps(value, default=str))
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str):
        """Delete data from cache"""
        if not self.redis_client:
            return
        
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate cache keys matching pattern"""
        if not self.redis_client:
            return
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            logger.error(f"Cache invalidate error: {e}")

cache = CacheManager()