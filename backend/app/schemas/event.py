"""Event Schemas."""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class EventBase(BaseModel):
    event_type: str = Field(..., description="Classification of the event", json_schema_extra={"example": "incident"})
    entity_type: Optional[str] = Field(None, description="Entity type affected", json_schema_extra={"example": "customer"})
    entity_id: Optional[str] = Field(None, description="Identifier of the entity affected", json_schema_extra={"example": "ACME Corp"})
    title: str = Field(..., description="Short title describing the event", json_schema_extra={"example": "Payment Gateway Failure"})
    description: Optional[str] = Field(None, description="Detailed event summary", json_schema_extra={"example": "Multiple recurring payment timeout errors on primary gateway."})
    source: str = Field("system", description="Source of event ingestion", json_schema_extra={"example": "monitoring"})
    metadata_json: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary event payload")


class EventCreate(EventBase):
    organization_id: uuid.UUID = Field(..., description="Owning organization ID")
    timestamp: Optional[datetime] = Field(default=None, description="Time of event occurrence")


class EventResponse(EventBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
