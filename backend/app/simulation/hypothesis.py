"""Hypothesis models and parameter overrides for counterfactual exploration."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CounterfactualHypothesis(BaseModel):
    hypothesis_id: str
    target_action: str
    condition_precedents: List[str] = Field(default_factory=list)
    altered_parameters: Dict[str, Any] = Field(default_factory=dict)
    rationale: str
    constraints: List[str] = Field(default_factory=list)
