import redis.asyncio as redis
from app.config import settings

redis_client = None

async def get_redis_client():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    return redis_client