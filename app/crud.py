from sqlalchemy.orm import Session
import logging
from . import models, schemas
from app.auth import get_password_hash # Import the hashing function

logger = logging.getLogger(__name__)

# Customer CRUD operations
def get_customer(db: Session, customer_id: int):
    """Retrieves a single customer by their ID."""
    logger.info(f"Fetching customer with id {customer_id}")
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str):
    """Retrieves a single customer by their email address."""
    logger.info(f"Fetching customer with email {email}")
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    """Retrieves a list of customers with pagination."""
    logger.info(f"Fetching customers with skip={skip}, limit={limit}")
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    """Creates a new customer in the database."""
    logger.info(f"Creating customer with email: {customer.email}")
    db_customer = models.Customer(**customer.dict()) # Use model_dump() for Pydantic v2
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer_update: schemas.CustomerCreate):
    """Updates an existing customer in the database."""
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer_update.dict(exclude_unset=True) # Use model_dump() for Pydantic v2
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    """Deletes a customer from the database."""
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer

# User CRUD operations
def get_user(db: Session, user_id: int):
    """Retrieves a single user by their ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Retrieves a single user by their username."""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Creates a new user in the database with a hashed password."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User {user.username} created successfully.")
    return db_user