"""Causal Edge definitions and relationship types."""

import uuid
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict


class CausalRelationshipType(str, Enum):
    CAUSES = "CAUSES"
    CONTRIBUTES_TO = "CONTRIBUTES_TO"
    TRIGGERS = "TRIGGERS"
    PRECEDED = "PRECEDED"
    FOLLOWED_BY = "FOLLOWED_BY"
    RESOLVED_BY = "RESOLVED_BY"
    FAILED_BECAUSE_OF = "FAILED_BECAUSE_OF"
    DEPENDS_ON = "DEPENDS_ON"
    CORRELATED_WITH = "CORRELATED_WITH"
    AMPLIFIES = "AMPLIFIES"
    MITIGATES = "MITIGATES"
    CONTRADICTS = "CONTRADICTS"
    RESULTED_IN = "RESULTED_IN"


class CausalEdgeDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str
    source_node_id: str
    target_node_id: str
    relationship: str
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    evidence: Dict[str, Any] = Field(default_factory=dict)
    source_type: str = "inference"
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
