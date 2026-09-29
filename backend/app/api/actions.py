"""Controlled Action Engine API Router."""

import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Action
from app.actions.action_engine import action_engine
from app.actions.validators import ActionValidationError
from app.schemas.action_api import (
    CreateActionRequest,
    ApproveActionRequest,
    RejectActionRequest,
    ExecuteActionRequest,
    ActionResponse,
)
from app.core.logging import logger

router = APIRouter(prefix="/actions", tags=["Controlled Action Engine"])


def _action_to_response(action: Action) -> ActionResponse:
    return ActionResponse(
        id=str(action.id),
        organization_id=str(action.organization_id),
        action_type=action.action_type,
        payload=action.payload or {},
        risk_level=action.risk_level,
        approval_required=action.approval_required,
        approval_status=action.approval_status,
        approved_by=action.approved_by,
        requested_by=action.requested_by,
        status=action.status,
        execution_status=action.execution_status,
        result=action.result,
        created_at=action.created_at.isoformat() if action.created_at else None,
        completed_at=action.completed_at.isoformat() if action.completed_at else None,
    )


from app.core.security import require_permission, Permission, AuthContext, get_current_auth
from app.services.audit_service import audit_service


@router.post("", response_model=ActionResponse, summary="Submit a Controlled Action Request")
def submit_action(
    payload: CreateActionRequest,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission(Permission.INVESTIGATE)),
):
    """Submits an action request, validates schema, evaluates human approval rules, and registers the action."""
    try:
        action = action_engine.request_action(
            db=db,
            organization_id=payload.organization_id,
            action_type=payload.action_type,
            parameters=payload.parameters,
            requested_by=payload.requested_by or auth.user_id,
            agent=payload.agent_id,
            decision_id=payload.decision_id,
            auto_execute_low_risk=payload.auto_execute_low_risk or False,
        )
        audit_service.log_event(
            db=db,
            organization_id=payload.organization_id,
            event_type="ACTION_SUBMITTED",
            user_id=auth.user_id,
            resource_type="action",
            resource_id=str(action.id),
            result="success",
            details={"action_type": action.action_type, "risk_level": action.risk_level},
        )
        return _action_to_response(action)
    except ActionValidationError as e:
        audit_service.log_event(
            db=db,
            organization_id=payload.organization_id,
            event_type="SECURITY_VIOLATION",
            user_id=auth.user_id,
            result="validation_failed",
            details={"error": str(e), "action_type": payload.action_type},
        )
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error submitting action: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{action_id}/approve", response_model=ActionResponse, summary="Human Approval for Action")
def approve_action(
    action_id: uuid.UUID,
    payload: ApproveActionRequest,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission(Permission.APPROVE)),
):
    """Applies human reviewer authorization to a pending action."""
    try:
        action = action_engine.approve_action(
            db=db,
            action_id=action_id,
            approved_by=payload.approved_by or auth.user_id,
            comment=payload.comment,
        )
        audit_service.log_event(
            db=db,
            organization_id=action.organization_id,
            event_type="APPROVAL_GRANTED",
            user_id=auth.user_id,
            resource_type="action",
            resource_id=str(action.id),
            result="success",
            details={"approved_by": action.approved_by, "comment": payload.comment},
        )
        return _action_to_response(action)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error approving action: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{action_id}/reject", response_model=ActionResponse, summary="Human Rejection for Action")
def reject_action(
    action_id: uuid.UUID,
    payload: RejectActionRequest,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission(Permission.APPROVE)),
):
    """Permanently rejects a pending action request."""
    try:
        action = action_engine.reject_action(
            db=db,
            action_id=action_id,
            rejected_by=payload.rejected_by or auth.user_id,
            reason=payload.reason,
        )
        audit_service.log_event(
            db=db,
            organization_id=action.organization_id,
            event_type="APPROVAL_REJECTED",
            user_id=auth.user_id,
            resource_type="action",
            resource_id=str(action.id),
            result="rejected",
            details={"rejected_by": action.approved_by, "reason": payload.reason},
        )
        return _action_to_response(action)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error rejecting action: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{action_id}/execute", response_model=ActionResponse, summary="Execute Authorized Action")
def execute_action(
    action_id: uuid.UUID,
    payload: ExecuteActionRequest,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission(Permission.EXECUTE)),
):
    """Safely executes an approved action against PostgreSQL state."""
    try:
        action = action_engine.execute_action(
            db=db,
            action_id=action_id,
            executed_by=payload.executed_by or auth.user_id,
        )
        audit_service.log_event(
            db=db,
            organization_id=action.organization_id,
            event_type="ACTION_EXECUTED",
            user_id=auth.user_id,
            resource_type="action",
            resource_id=str(action.id),
            result="success",
            details={"action_type": action.action_type, "result": action.result},
        )
        return _action_to_response(action)
    except ActionValidationError as e:
        audit_service.log_event(
            db=db,
            organization_id=auth.organization_id,
            event_type="ACTION_FAILED",
            user_id=auth.user_id,
            resource_type="action",
            resource_id=str(action_id),
            result="validation_error",
            details={"error": str(e)},
        )
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing action: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=list[ActionResponse], summary="List Controlled Actions")
def list_actions(
    organization_id: Optional[uuid.UUID] = None,
    status: Optional[str] = None,
    approval_status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Lists registered actions with optional filtering by status or approval status."""
    query = db.query(Action)
    if organization_id:
        query = query.filter(Action.organization_id == organization_id)
    if status:
        query = query.filter(Action.status == status)
    if approval_status:
        query = query.filter(Action.approval_status == approval_status)
    actions = query.order_by(Action.created_at.desc()).limit(limit).all()
    return [_action_to_response(a) for a in actions]


@router.get("/{action_id}", response_model=ActionResponse, summary="Get Action Details")
def get_action(action_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retrieves full details for a specific action."""
    action = db.get(Action, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return _action_to_response(action)
