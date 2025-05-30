from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.config import settings
from app.core.redis_config import get_redis_client

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis_client)
):
    try:
        # Check database connection
        await db.execute("SELECT 1")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {e}"
        )

    try:
        # Check Redis connection
        await redis_client.ping()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Redis connection failed: {e}"
        )

    return {"status": "ok", "database": "connected", "redis": "connected"}
