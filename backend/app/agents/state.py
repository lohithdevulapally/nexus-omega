"""Shared Agent State and Data Transfer Models for NEXUS-Ω Multi-Agent System."""

import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    memory_id: str
    source: str = "hindsight"
    relevance: float = 0.9
    confidence: float = 0.95
    timestamp: Optional[str] = None
    summary: str
    outcome: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class MemoryConflict(BaseModel):
    conflict: bool = False
    memories: List[Dict[str, Any]] = Field(default_factory=list)
    explanation: Optional[str] = None
    resolution_strategy: str = "requires_context"  # "requires_context", "temporal_precedence", "manual_override"


class MemoryProvenance(BaseModel):
    recommendation: str
    evidence_items: List[Dict[str, Any]] = Field(default_factory=list)
    hindsight_memories: List[str] = Field(default_factory=list)
    postgres_experiences: List[str] = Field(default_factory=list)
    confidence: float = 0.95


class CausalRelationship(BaseModel):
    source_event: str
    target_event: str
    relationship: str  # CAUSES, PRECEDED, CORRELATED_WITH, RESOLVED_BY, FAILED_BECAUSE_OF, DEPENDS_ON, TRIGGERED, CONTRADICTS
    evidence: str
    confidence: float = 0.90


class RiskItem(BaseModel):
    risk_type: str  # recurrence_risk, customer_impact, operational_risk, financial_risk, cascading_risk, historical_failure_risk
    description: str
    severity: str  # low, medium, high, critical
    probability_estimate: str  # low, medium, high (data-grounded)
    evidence: str
    mitigation: str


class DecisionCandidate(BaseModel):
    decision_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action: str
    rationale_summary: str
    expected_outcome: str
    historical_support: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    confidence: float = 0.90
    approval_required: bool = False


class TimelineStep(BaseModel):
    step: int
    agent: str
    status: str = "completed"
    duration_ms: float = 0.0
    memories_used: int = 0
    summary: str = ""


class AgentState(BaseModel):
    # Request Identifiers
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: uuid.UUID
    user_id: Optional[str] = None
    user_request: str

    # Context & Memories
    current_context: Dict[str, Any] = Field(default_factory=dict)
    recalled_memories: List[MemoryItem] = Field(default_factory=list)
    memory_references: List[Dict[str, Any]] = Field(default_factory=list)
    memory_conflicts: List[MemoryConflict] = Field(default_factory=list)

    # Agent Step Outputs
    planner_output: Dict[str, Any] = Field(default_factory=dict)
    analyst_output: Dict[str, Any] = Field(default_factory=dict)
    causal_output: Dict[str, Any] = Field(default_factory=dict)
    simulation_output: Optional[Dict[str, Any]] = None
    risk_output: Dict[str, Any] = Field(default_factory=dict)
    decision_output: Dict[str, Any] = Field(default_factory=dict)
    critic_output: Dict[str, Any] = Field(default_factory=dict)

    # Decision, Action & Execution
    final_recommendation: Optional[str] = None
    provenance: Optional[MemoryProvenance] = None
    approval_required: bool = False
    approval_status: str = "pending"  # pending, approved, rejected, not_required
    action_request: Optional[Dict[str, Any]] = None
    action_id: Optional[str] = None
    execution_result: Optional[Dict[str, Any]] = None
    reflection_result: Optional[Dict[str, Any]] = None

    # Audit & Observability
    timeline: List[TimelineStep] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    status: str = "initialized"  # initialized, planning, analyzing, deciding, completed, failed
    timestamps: Dict[str, str] = Field(
        default_factory=lambda: {"started_at": datetime.now(timezone.utc).isoformat()}
    )
