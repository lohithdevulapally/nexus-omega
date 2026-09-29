"""Schemas for Controlled Action Engine API."""

import uuid
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class CreateActionRequest(BaseModel):
    organization_id: uuid.UUID = Field(..., description="Organization identifier")
    action_type: str = Field(..., description="Whitelisted action type")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Action payload parameters")
    requested_by: Optional[str] = Field("operator", description="User or agent requesting action")
    agent_id: Optional[str] = Field(None, description="Agent identifier if initiated by an agent")
    decision_id: Optional[uuid.UUID] = Field(None, description="Associated Decision ID if applicable")
    auto_execute_low_risk: Optional[bool] = Field(False, description="Automatically execute if risk is low and no approval needed")


class ApproveActionRequest(BaseModel):
    approved_by: str = Field(..., description="Identifier or name of human reviewer")
    comment: Optional[str] = Field(None, description="Optional approval comments")


class RejectActionRequest(BaseModel):
    rejected_by: str = Field(..., description="Identifier or name of human reviewer")
    reason: str = Field(..., description="Mandatory reason for rejection")


class ExecuteActionRequest(BaseModel):
    executed_by: Optional[str] = Field("operator", description="Executing entity")


class ActionResponse(BaseModel):
    id: str
    organization_id: str
    action_type: str
    payload: Dict[str, Any]
    risk_level: str
    approval_required: bool
    approval_status: str
    approved_by: Optional[str] = None
    requested_by: Optional[str] = None
    status: str
    execution_status: str
    result: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
