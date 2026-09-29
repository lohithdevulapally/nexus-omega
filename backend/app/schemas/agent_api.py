"""Agent API Schemas for Multi-Agent Decision Intelligence."""

import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from app.agents.state import MemoryItem, TimelineStep, MemoryProvenance


class AgentInvestigateRequest(BaseModel):
    organization_id: uuid.UUID = Field(..., description="Organization identifier", json_schema_extra={"example": "2d48f08c-0b35-4aea-8941-86e4f855f738"})
    user_id: Optional[str] = Field(None, description="Requesting user ID", json_schema_extra={"example": "user-123"})
    request: str = Field(..., description="Operational incident or objective to investigate", json_schema_extra={"example": "ACME is experiencing payment failures again. Investigate what happened historically and recommend what we should do."})


class AgentInvestigateResponse(BaseModel):
    request_id: str
    status: str
    plan: Dict[str, Any]
    memories: List[MemoryItem]
    findings: List[str]
    causal_analysis: Dict[str, Any]
    risks: Dict[str, Any]
    decision_candidates: List[Dict[str, Any]]
    critique: Dict[str, Any]
    final_recommendation: str
    approval_required: bool
    provenance: Optional[MemoryProvenance] = None
    simulation: Optional[Dict[str, Any]] = None
    action_id: Optional[str] = None
    action_request: Optional[Dict[str, Any]] = None
    timeline: List[TimelineStep]
