from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime # Add DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # Import func for server_default
from .database import Base


class Customer(Base):
    """SQLAlchemy model for a customer."""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    company_name = Column(String, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class User(Base):
    """SQLAlchemy model for a user."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # Add more fields like email, full_name, roles etc. if needed