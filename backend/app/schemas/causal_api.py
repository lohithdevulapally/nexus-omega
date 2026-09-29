"""Schemas for Causal Knowledge Graph API."""

import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class RootCauseRequest(BaseModel):
    organization_id: uuid.UUID = Field(..., description="Organization identifier")
    incident_id: str = Field(..., description="Incident label or entity ID to analyze")
    depth: int = Field(default=5, ge=1, le=10, description="Max traversal depth")


class RootCauseResponse(BaseModel):
    incident: str
    immediate_cause: Optional[str] = None
    root_causes: List[Dict[str, Any]] = Field(default_factory=list)
    contributing_factors: List[Dict[str, Any]] = Field(default_factory=list)
    upstream_causes: List[Dict[str, Any]] = Field(default_factory=list)
    downstream_effects: List[Dict[str, Any]] = Field(default_factory=list)
    symptoms: List[Dict[str, Any]] = Field(default_factory=list)
    unresolved_hypotheses: List[Dict[str, Any]] = Field(default_factory=list)
    confidence: float


class CausalPathResponse(BaseModel):
    source: str
    target: str
    path_count: int
    paths: List[Dict[str, Any]] = Field(default_factory=list)


class CascadeRequest(BaseModel):
    organization_id: uuid.UUID = Field(..., description="Organization identifier")
    trigger: str = Field(..., description="Trigger event or action to propagate")
    depth: int = Field(default=5, ge=1, le=10, description="Propagation depth")


class CascadeResponse(BaseModel):
    trigger: str
    severity: str
    cascade_paths: List[str] = Field(default_factory=list)
    affected_entities: List[Dict[str, Any]] = Field(default_factory=list)
    total_downstream_entities: int
    evidence: Dict[str, Any] = Field(default_factory=dict)
