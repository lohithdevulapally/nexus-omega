"""Human Approval System for high-impact and consequential actions."""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.core.logging import logger


class HumanApprovalSystem:
    """Manages human approval lifecycle ensuring no consequential actions execute unverified."""

    @classmethod
    def evaluate_approval_requirement(
        cls, risk_tier: str, action_type: str, explicit_requires_approval: Optional[bool] = None
    ) -> bool:
        """Determines if human review is strictly mandatory."""
        if explicit_requires_approval is not None:
            return explicit_requires_approval

        if risk_tier in {"medium", "high", "critical"}:
            logger.info(f"[APPROVAL_REQUIRED] Action='{action_type}' Tier='{risk_tier}' mandates human authorization.")
            return True

        return False

    @classmethod
    def process_approval(
        cls, action_dict: Dict[str, Any], approved_by: str, comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """Applies human approval."""
        if action_dict.get("status") in {"executed", "completed"}:
            raise ValueError("Action has already completed.")
        if action_dict.get("approval_status") == "approved" and action_dict.get("approved_by"):
            raise ValueError(f"Action has already been approved by '{action_dict.get('approved_by')}'.")

        now_iso = datetime.now(timezone.utc).isoformat()
        logger.info(f"[ACTION_VALIDATION] ActionID={action_dict.get('id')} APPROVED by '{approved_by}'")

        return {
            "approval_status": "approved",
            "approved_by": approved_by,
            "status": "approved",
            "approval_comment": comment or "Authorized via Human-in-the-Loop approval gate.",
            "approved_at": now_iso,
        }

    @classmethod
    def process_rejection(
        cls, action_dict: Dict[str, Any], rejected_by: str, reason: str
    ) -> Dict[str, Any]:
        """Applies human rejection."""
        now_iso = datetime.now(timezone.utc).isoformat()
        logger.info(f"[ACTION_VALIDATION] ActionID={action_dict.get('id')} REJECTED by '{rejected_by}' Reason='{reason}'")

        return {
            "approval_status": "rejected",
            "status": "rejected",
            "rejected_by": rejected_by,
            "rejection_reason": reason,
            "rejected_at": now_iso,
        }
