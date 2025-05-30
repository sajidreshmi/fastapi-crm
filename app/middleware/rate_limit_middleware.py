from fastapi import Request, HTTPException, status
from app.core.redis_config import redis_client


async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    # Simple rate limiting: 5 requests per minute per IP
    key = f"rate_limit:{client_ip}"
    # Increment the counter for the IP
    current_requests = await redis_client.incr(key)
    if current_requests == 1:
        # Set expiry for the first request in the window
        await redis_client.expire(key, 60)  # 60 seconds

    if current_requests > 20:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")

    response = await call_next(request)
    return response
