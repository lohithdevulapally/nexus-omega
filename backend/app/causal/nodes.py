"""Causal Node definitions and data transfer objects."""

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class CausalEntityType(str, Enum):
    ORGANIZATION = "Organization"
    CUSTOMER = "Customer"
    EVENT = "Event"
    INCIDENT = "Incident"
    EXPERIENCE = "Experience"
    DECISION = "Decision"
    ACTION = "Action"
    OUTCOME = "Outcome"
    SYSTEM = "System"
    SERVICE = "Service"
    FAILURE = "Failure"
    RISK = "Risk"
    AGENT_RUN = "AgentRun"
    UNKNOWN = "Unknown"


class CausalNodeDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str
    entity_type: str
    entity_id: Optional[str] = None
    label: str
    description: Optional[str] = None
    metadata_json: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
