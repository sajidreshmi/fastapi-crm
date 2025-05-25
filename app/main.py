from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

from .database import engine, Base # Ensure Base is imported
from .routers import customers, auth # Import the new auth router
from . import models # Import models to ensure tables are created

# Create database tables if they don't exist
# This should ideally be handled by migrations (e.g. Alembic) in a production app
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Logging Configuration (basic)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom Exception Handler for Validation Errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()} for request: {request.url}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

# Generic Exception Handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc} for request: {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )

app.include_router(customers.router)
app.include_router(auth.router) # Include the auth router

@app.get("/")
async def root():
    return {"message": "Welcome to the CRM API"}

# To run this app, navigate to the py-fastapi-web directory and run:
# uvicorn app.main:app --reload