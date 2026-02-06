import os
import time
import uuid
import redis
import logging
from fastapi import Request
from fastapi.responses import Response

# Starlette tool for intercepting requests.
from starlette.middleware.base import BaseHTTPMiddleware 

# setup a logger
logger = logging.getLogger("api_gateway")
logging.basicConfig(level=logging.INFO)

class RequestLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Start timer
        start_time = time.time()

        # 2. Generate/retrieve correlation id
        if request.headers.get("X-Request-ID"):
            correlation_id = request.headers.get("X-Request-ID")
        else :
            correlation_id = str(uuid.uuid4())

        # 3. Log the incoming request
        logger.info(f"Incoming Request: {request.method} {request.url.path} | ID: {correlation_id}")

        # 4. Process the request 
        # pass it to the next layer
        response = await call_next(request)

        # 5. Calculate processing time
        process_time = time.time() - start_time

        # 6. Add the correlation id to response header 
        # so that client sees it too
        response.headers["X-Request-ID"] = correlation_id

        logger.info(f"Completed: {response.status_code} | Duration: {process_time:.4f} | ID: {correlation_id}")

        return response
    
# rate limiter
# 0. Get REDIS_HOST env variable
host = os.getenv("REDIS_HOST", "localhost")
# 1. Connect to Docker Redis
client = redis.Redis(host=host, port=6379, decode_responses=True)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        # Get the user's IP address to use as an ID 
        client_ip = request.client.host
        
        # create a key specifically for this user
        key = f"rate_limit:{client_ip}"

        # Increment the count for the key
        current_key_val = client.incr(key)

        # set TTL for first request
        if current_key_val == 1:
            client.expire(key, 60)
        
        # if count > 5 return 429 error
        if current_key_val > 5:
            return Response("Rate Limit Exceeded", status_code=429)
        
        response = await call_next(request)
        return response