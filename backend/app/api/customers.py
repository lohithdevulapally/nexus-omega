"""Customer API Router."""

import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import get_db
from app.db.models import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=CustomerResponse, summary="Create Customer")
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    """Creates a new customer record."""
    customer = Customer(
        organization_id=payload.organization_id,
        name=payload.name,
        industry=payload.industry,
        status=payload.status,
        risk_level=payload.risk_level,
        metadata_json=payload.metadata_json,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/{id}", response_model=CustomerResponse, summary="Get Customer By ID")
def get_customer(id: uuid.UUID, db: Session = Depends(get_db)):
    """Retrieves customer structured profile by ID."""
    customer = db.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


from typing import List, Optional
from app.core.security import get_current_auth, AuthContext


@router.get("", response_model=List[CustomerResponse], summary="List Customers")
def list_customers(
    organization_id: Optional[uuid.UUID] = Query(None, description="Organization ID"),
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(get_current_auth),
):
    """Lists all customers for an organization."""
    target_org = organization_id or auth.organization_id
    stmt = select(Customer).where(Customer.organization_id == target_org)
    return list(db.scalars(stmt).all())
