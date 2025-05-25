from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Base schema for Customer
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    company_name: Optional[str] = None

# Schema for creating a customer
class CustomerCreate(CustomerBase):
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
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True # Changed from from_attributes = True for Pydantic v1 compatibility if needed, orm_mode for v2+

# You can add other schemas here

# New Schemas for User and Token
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None