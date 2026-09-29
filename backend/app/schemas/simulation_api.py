"""Schemas for Counterfactual Simulation API."""

import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from app.simulation.simulation_models import ScenarioOptionEvaluation


class CounterfactualRequest(BaseModel):
    organization_id: uuid.UUID = Field(..., description="Organization identifier")
    incident_id: Optional[str] = Field("ACME Payment Gateway Outage", description="Incident identifier or description")
    alternative_action: str = Field(..., description="Alternative action to test (e.g. 'restart_gateway')")
    baseline_action: Optional[str] = Field("switch_to_secondary_rail_b", description="Baseline action")


class CounterfactualResponse(BaseModel):
    actual_world: Dict[str, Any]
    counterfactual_world: Dict[str, Any]
    differences: List[str]
    causal_paths: List[str]
    historical_evidence: List[Any]
    assumptions: List[str]
    uncertainty: List[str]
    confidence: float


class CompareScenariosRequest(BaseModel):
    organization_id: uuid.UUID = Field(..., description="Organization identifier")
    decision_context: str = Field(..., description="Decision context or operational incident")
    options: List[str] = Field(..., min_length=2, description="Candidate action options to evaluate")


class CompareScenariosResponse(BaseModel):
    comparison_id: str
    decision_context: str
    timestamp: str
    options_evaluated: List[ScenarioOptionEvaluation] = Field(default_factory=list)
    evaluations: List[ScenarioOptionEvaluation] = Field(default_factory=list)
    comparative_synthesis: str

    def model_post_init(self, __context: Any) -> None:
        if not self.evaluations and self.options_evaluated:
            self.evaluations = self.options_evaluated
        elif not self.options_evaluated and self.evaluations:
            self.options_evaluated = self.evaluations


class ReconstructStateRequest(BaseModel):
    organization_id: uuid.UUID = Field(..., description="Organization identifier")
    timestamp: str = Field(..., description="ISO 8601 timestamp for historical state reconstruction")


class ReconstructStateResponse(BaseModel):
    snapshot_id: str
    organization_id: str
    timestamp: str
    source_request: str
    simulation_tag: str
    state_hash: str
    entities: Dict[str, Any]
    events: List[Dict[str, Any]]
    experiences: List[Dict[str, Any]]
    active_risks: List[Dict[str, Any]]
    relevant_memories: List[Dict[str, Any]]
