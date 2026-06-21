#backend/app/utils/rate_limiter.py
from fastapi import HTTPException, Request
from functools import wraps
from collections import defaultdict
import time
import threading

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_allowed(self, client_ip: str) -> bool:
        with self.lock:
            now = time.time()
            minute_ago = now - 60
            
            # Xóa requests cũ
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if req_time > minute_ago
            ]
            
            # Kiểm tra limit
            if len(self.requests[client_ip]) >= self.requests_per_minute:
                return False
            
            self.requests[client_ip].append(now)
            return True

rate_limiter = RateLimiter(requests_per_minute=30)

def rate_limit(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        client_ip = request.client.host
        if not rate_limiter.is_allowed(client_ip):
            raise HTTPException(status_code=429, detail="Too many requests")
        return await func(request, *args, **kwargs)
    return wrapper