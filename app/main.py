from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from .middleware.auth_middleware import auth_middleware
from .middleware.logging_middleware import logging_middleware
from .middleware.error_handling_middleware import error_handling_middleware
from .middleware.rate_limit_middleware import rate_limit_middleware
import logging
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter

from .database import engine, Base  # Ensure Base is imported
from .routers.v1 import customers, auth, health  # Import the new auth router
from . import models  # Import models to ensure tables are created
from .config import settings
from .core.redis_config import get_redis_client  # Import get_redis_client

# Create database tables if they don't exist
# This should ideally be handled by migrations (e.g. Alembic) in a production app
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRM API",
    description="A simple CRM API with customer and user management.",
    version="0.1.0",
)

# Add middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=error_handling_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)

# Logging Configuration (basic)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    redis_client = await get_redis_client()
    await FastAPILimiter.init(redis_client)

# Custom Exception Handler for Validation Errors


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles FastAPI request validation errors, returning a 422 response."""
    logger.error(
        f"Validation error: {exc.errors()} for request: {request.url}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

# Generic Exception Handler


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handles any other unhandled exceptions, returning a 500 response."""
    logger.error(f"Unhandled exception: {exc} for request: {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(health.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint for the API."""
    return {"message": "Welcome to the CRM API"}
# To run this app, navigate to the py-fastapi-web directory and run:
# uvicorn app.main:app --reload
