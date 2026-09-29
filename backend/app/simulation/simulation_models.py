"""Models and schemas for Counterfactual Simulation and Scenario Comparison."""

import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CounterfactualScenario(BaseModel):
    scenario_id: str = Field(default_factory=lambda: f"scen-{uuid.uuid4().hex[:8]}")
    name: str
    description: str
    baseline_action: str
    alternative_action: str
    assumptions: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    starting_state: Dict[str, Any] = Field(default_factory=dict)
    historical_evidence: List[Dict[str, Any]] = Field(default_factory=list)


class SimulationResult(BaseModel):
    simulation_id: str = Field(default_factory=lambda: f"sim-{uuid.uuid4().hex[:8]}")
    scenario: CounterfactualScenario
    expected_effects: List[str] = Field(default_factory=list)
    risks: List[Dict[str, Any]] = Field(default_factory=list)
    downstream_impacts: List[Dict[str, Any]] = Field(default_factory=list)
    supporting_evidence: List[Any] = Field(default_factory=list)
    uncertainty: List[str] = Field(default_factory=list)
    confidence: float = 0.85

    # Mandatory structural differentiation
    observed_facts: List[str] = Field(default_factory=list)
    historical_analogues: List[str] = Field(default_factory=list)
    simulation_assumptions: List[str] = Field(default_factory=list)
    projected_outcomes: List[str] = Field(default_factory=list)


class ScenarioOptionEvaluation(BaseModel):
    option: str
    action: Optional[str] = None
    assumptions: List[str] = Field(default_factory=list)
    projected_outcomes: List[str] = Field(default_factory=list)
    projected_outcome: Optional[str] = None
    risk_propagation: List[Dict[str, Any]] = Field(default_factory=list)
    risk_severity: Optional[str] = None
    historical_evidence: List[Any] = Field(default_factory=list)
    uncertainty: List[str] = Field(default_factory=list)
    reversibility: str = "high"  # high, medium, low, irreversible
    required_approval: bool = False
    affected_entities: List[str] = Field(default_factory=list)
    confidence: float = 0.85

    def model_post_init(self, __context: Any) -> None:
        if not self.action:
            self.action = self.option
        if not self.projected_outcome:
            self.projected_outcome = self.projected_outcomes[0] if self.projected_outcomes else "No outcome projected"
        if not self.risk_severity:
            if self.risk_propagation and isinstance(self.risk_propagation[0], dict):
                self.risk_severity = self.risk_propagation[0].get("severity", "medium").upper()
            else:
                self.risk_severity = "MEDIUM"


class MultiScenarioComparison(BaseModel):
    comparison_id: str = Field(default_factory=lambda: f"cmp-{uuid.uuid4().hex[:8]}")
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
