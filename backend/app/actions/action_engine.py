"""ActionEngine orchestrating validation, approval, and controlled execution."""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import Action
from app.actions.action_registry import ActionRegistry, ActionRiskTier
from app.actions.validators import ActionValidator
from app.actions.approval import HumanApprovalSystem
from app.actions.executor import ActionExecutor
from app.core.logging import logger


class ActionEngine:
    """End-to-end lifecycle coordinator for controlled enterprise actions."""

    @classmethod
    def request_action(
        cls,
        db: Session,
        organization_id: uuid.UUID,
        action_type: str,
        parameters: Dict[str, Any],
        requested_by: Optional[str] = "system",
        agent: Optional[str] = None,
        decision_id: Optional[uuid.UUID] = None,
        auto_execute_low_risk: bool = False,
        risk_level: Optional[str] = None,
        approval_required: Optional[bool] = None,
    ) -> Action:
        """Submits a new action request, validates schema, evaluates approval, and persists to DB."""
        # 1. Validate schema & constraints
        validation = ActionValidator.validate_request(
            action_type=action_type,
            parameters=parameters,
            requested_by=requested_by,
            agent=agent,
        )

        risk_tier = risk_level or validation["risk_tier"]
        if approval_required is None:
            approval_required = HumanApprovalSystem.evaluate_approval_requirement(
                risk_tier=risk_tier,
                action_type=action_type,
                explicit_requires_approval=validation["requires_human_approval"],
            )

        initial_status = "pending"
        approval_status = "pending" if approval_required else "approved"
        execution_status = "not_started"

        action = Action(
            id=uuid.uuid4(),
            organization_id=organization_id,
            decision_id=decision_id,
            agent_id=agent,
            action_type=action_type,
            payload=parameters,
            approval_required=approval_required,
            approval_status=approval_status,
            requested_by=requested_by,
            risk_level=risk_tier,
            status=initial_status,
            execution_status=execution_status,
        )
        db.add(action)
        db.flush()

        # 2. Auto-execute if low-risk and approved
        if auto_execute_low_risk and not approval_required:
            action = cls.execute_action(db=db, action_id=action.id, executed_by=requested_by or "system")

        db.commit()
        db.refresh(action)
        return action

    @classmethod
    def approve_action(
        cls, db: Session, action_id: uuid.UUID, approved_by: str, comment: Optional[str] = None
    ) -> Action:
        """Applies human approval and prepares action for execution."""
        action = db.get(Action, action_id)
        if not action:
            raise ValueError(f"Action with ID '{action_id}' not found.")

        updates = HumanApprovalSystem.process_approval(
            action_dict={"id": str(action.id), "status": action.status, "approval_status": action.approval_status},
            approved_by=approved_by,
            comment=comment,
        )

        action.approval_status = updates["approval_status"]
        action.approved_by = updates["approved_by"]
        action.status = updates["status"]
        db.commit()
        db.refresh(action)
        return action

    @classmethod
    def reject_action(
        cls, db: Session, action_id: uuid.UUID, rejected_by: str, reason: str
    ) -> Action:
        """Applies human rejection, permanently halting execution."""
        action = db.get(Action, action_id)
        if not action:
            raise ValueError(f"Action with ID '{action_id}' not found.")

        updates = HumanApprovalSystem.process_rejection(
            action_dict={"id": str(action.id), "status": action.status},
            rejected_by=rejected_by,
            reason=reason,
        )

        action.approval_status = updates["approval_status"]
        action.status = updates["status"]
        action.execution_status = "rejected"
        action.result = {"rejection_reason": reason, "rejected_by": rejected_by}
        db.commit()
        db.refresh(action)
        return action

    @classmethod
    def execute_action(
        cls, db: Session, action_id: uuid.UUID, executed_by: str = "operator"
    ) -> Action:
        """Validates pre-flight state and safely executes the action."""
        action = db.get(Action, action_id)
        if not action:
            raise ValueError(f"Action with ID '{action_id}' not found.")

        ActionValidator.validate_execution(
            action_status=action.status,
            approval_status=action.approval_status,
            approval_required=action.approval_required,
        )

        # Execute
        result = ActionExecutor.execute(
            db=db,
            organization_id=action.organization_id,
            action_type=action.action_type,
            parameters=action.payload,
            action_id=str(action.id),
        )

        action.status = "executed"
        action.execution_status = "completed"
        action.completed_at = datetime.now(timezone.utc)
        action.result = result
        db.commit()
        db.refresh(action)
        return action


action_engine = ActionEngine()
