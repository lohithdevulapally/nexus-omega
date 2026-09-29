"""Investigation Schemas for 'Have We Seen This Before?' and 'Don't Repeat Our Mistake'."""

import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from app.agents.state import MemoryProvenance


class SimilarIncidentRequest(BaseModel):
    organization_id: uuid.UUID = Field(
        ...,
        description="Organization ID",
        json_schema_extra={"example": "11111111-1111-1111-1111-111111111111"},
    )
    description: str = Field(
        ...,
        description="Description of the current incident or situation",
        json_schema_extra={"example": "ACME is experiencing payment failures again."},
    )


class SimilarIncidentResponse(BaseModel):
    similarity_found: bool
    historical_cases: List[Dict[str, Any]] = Field(default_factory=list)
    common_patterns: List[str] = Field(default_factory=list)
    differences: List[str] = Field(default_factory=list)
    previous_outcomes: List[str] = Field(default_factory=list)
    relevant_memory: List[Dict[str, Any]] = Field(default_factory=list)
    analysis_summary: str
    # Upgraded agent intelligence fields
    similarity_explanation: Optional[str] = None
    previous_actions: List[str] = Field(default_factory=list)
    outcomes: List[str] = Field(default_factory=list)
    lessons_learned: List[str] = Field(default_factory=list)
    recurrence_indicators: List[str] = Field(default_factory=list)
    confidence: float = 0.95
    provenance: Optional[MemoryProvenance] = None


class AvoidMistakesRequest(BaseModel):
    organization_id: uuid.UUID = Field(
        ...,
        description="Organization ID",
        json_schema_extra={"example": "11111111-1111-1111-1111-111111111111"},
    )
    proposed_action: str = Field(
        ...,
        description="Action under consideration",
        json_schema_extra={"example": "Restart the payment service."},
    )


class AvoidMistakesResponse(BaseModel):
    warning: bool
    reason: str
    historical_cases: List[Dict[str, Any]] = Field(default_factory=list)
    alternative_successful_actions: List[str] = Field(default_factory=list)
    confidence: float = 0.95
    # Upgraded agent intelligence fields
    historical_failure: Optional[str] = None
    why_it_failed: Optional[str] = None
    conditions_under_which_it_failed: Optional[str] = None
    current_similarity: Optional[str] = None
    safer_alternatives: List[str] = Field(default_factory=list)
