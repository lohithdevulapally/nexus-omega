"""Customer Schemas."""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class CustomerBase(BaseModel):
    name: str = Field(..., description="Customer legal or trading name", json_schema_extra={"example": "ACME Corp"})
    industry: Optional[str] = Field(None, description="Industry sector", json_schema_extra={"example": "E-commerce"})
    status: str = Field("active", description="Account status", json_schema_extra={"example": "active"})
    risk_level: str = Field("low", description="Risk assessment level", json_schema_extra={"example": "high"})
    metadata_json: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata attributes")


class CustomerCreate(CustomerBase):
    organization_id: uuid.UUID = Field(..., description="Owning organization ID")


class CustomerResponse(CustomerBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
