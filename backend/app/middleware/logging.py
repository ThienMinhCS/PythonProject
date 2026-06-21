#backend/app/middleware/logging.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
import json

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        body = await request.body()
        logger.info(f"Request: {request.method} {request.url.path}")
        if body:
            try:
                logger.debug(f"Body: {json.loads(body)}")
            except:
                logger.debug(f"Body: {body}")
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
        
        return response