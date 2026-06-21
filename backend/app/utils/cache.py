#backend/app/utils/cache.py
import redis
import json
from typing import Optional, Any
from app.config import settings

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[Any]:
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    
    def set(self, key: str, value: Any, expire: int = 300):
        self.redis_client.setex(key, expire, json.dumps(value))
    
    def delete(self, key: str):
        self.redis_client.delete(key)
    
    def clear_pattern(self, pattern: str):
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)

cache = CacheService()