from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum, IntEnum

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class PriorityInt(IntEnum):
    low = 1
    medium = 2
    high = 3



# Base schema for Customer
class CustomerBase(BaseModel):
    """Base Pydantic model for customer data."""
    first_name: str = Field(..., min_length=1, max_length=15, description="First name of the customer")
    last_name: str = Field(..., min_length=1, max_length=15, description="Last name of the customer")
    email: EmailStr = Field(..., description="Email address of the customer")
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15, description="Phone number of the customer")
    company_name: Optional[str] = Field(None, min_length=1, max_length=50, description="Company name of the customer")
    is_active: bool = Field(default=True, description="Active status of the customer")
    
# Schema for creating a customer
class CustomerCreate(CustomerBase):
    """Pydantic model for creating a new customer."""
    pass

# Schema for updating a customer (all fields optional)
class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    company_name: Optional[str] = None

# Schema for reading/returning a customer (includes id and timestamps)
class Customer(CustomerBase):
    """Pydantic model for representing a customer, including ID and active status."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True # Changed from from_attributes = True for Pydantic v1 compatibility if needed, orm_mode for v2+

# You can add other schemas here

# Schemas for User and Token
class UserBase(BaseModel):
    """Base Pydantic model for user data."""
    username: str

class UserCreate(UserBase):
    """Pydantic model for creating a new user, including password."""
    password: str

class User(UserBase):
    """Pydantic model for representing a user, including ID and active status."""
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    """Pydantic model for the access token response."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Pydantic model for data encoded in the JWT token (username)."""
    username: Optional[str] = None