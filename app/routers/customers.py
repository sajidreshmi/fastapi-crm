from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas, auth # Import auth
from app.database import SessionLocal

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    # dependencies=[Depends(auth.get_current_active_user)], # Apply to all routes in this router
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Customer)
def create_customer_endpoint(customer: schemas.CustomerCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """Creates a new customer. Requires authentication."""
    db_customer = crud.get_customer_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_customer(db=db, customer=customer)

@router.get("/", response_model=List[schemas.Customer])
def read_customers_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """Retrieves a list of customers. Requires authentication."""
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer_endpoint(customer_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """Retrieves a specific customer by ID. Requires authentication."""
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer_endpoint(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """Updates an existing customer. Requires authentication."""
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.update_customer(db=db, customer_id=customer_id, customer_update=customer)

@router.delete("/{customer_id}", response_model=schemas.Customer)
def delete_customer_endpoint(customer_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """Deletes a customer. Requires authentication."""
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.delete_customer(db=db, customer_id=customer_id)