"""Action Validators enforcing parameter integrity, permission boundaries, and safety constraints."""

from typing import Dict, Any, List, Optional
from app.actions.action_registry import ActionRegistry, ActionRiskTier
from app.core.logging import logger


class ActionValidationError(Exception):
    """Raised when an action request violates validation, schema, or safety constraints."""
    pass


class ActionValidator:
    """Pre-execution validation engine."""

    @classmethod
    def validate_request(
        cls,
        action_type: str,
        parameters: Dict[str, Any],
        requested_by: Optional[str] = None,
        agent: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Validates that an action conforms to schema and safety rules."""
        logger.info(f"[ACTION_VALIDATION] Validating Action='{action_type}' RequestedBy='{requested_by}' Agent='{agent}'")

        # 1. Whitelist check
        if not ActionRegistry.is_registered(action_type):
            raise ActionValidationError(
                f"Action type '{action_type}' is not recognized or permitted. Arbitrary commands are strictly forbidden."
            )

        spec = ActionRegistry.get_action_spec(action_type)

        # 2. Required parameters check
        required_params = spec.get("required_parameters", [])
        missing = [p for p in required_params if p not in parameters or parameters[p] is None]
        if missing:
            raise ActionValidationError(
                f"Action '{action_type}' is missing mandatory parameters: {', '.join(missing)}."
            )

        # 3. Allowed parameters check (disallows unrecognized extra keys)
        allowed_params = set(spec.get("allowed_parameters", []))
        unexpected = [p for p in parameters.keys() if p not in allowed_params]
        if unexpected:
            raise ActionValidationError(
                f"Action '{action_type}' received disallowed parameters: {', '.join(unexpected)}."
            )

        # 4. Security check on parameters: block shell injection or command patterns
        dangerous_patterns = [";", "&&", "||", "`", "$(", "rm -rf", "drop table", "truncate"]
        param_str = str(parameters).lower()
        if any(pat in param_str for pat in dangerous_patterns):
            raise ActionValidationError("Action parameters contain potentially hazardous command strings.")

        return {
            "valid": True,
            "action_type": action_type,
            "risk_tier": spec.get("risk_tier", ActionRiskTier.LOW.value),
            "requires_human_approval": spec.get("requires_human_approval", False),
        }

    @classmethod
    def validate_execution(
        cls,
        action_status: str,
        approval_status: str,
        approval_required: bool,
    ) -> bool:
        """Validates if an action is ready for physical execution."""
        if action_status in {"executed", "completed"}:
            raise ActionValidationError("Action has already been executed. Duplicate execution prevented.")

        if action_status in {"rejected", "cancelled"}:
            raise ActionValidationError(f"Cannot execute action with status '{action_status}'.")

        if approval_required and approval_status != "approved":
            raise ActionValidationError(
                f"Action requires human approval before execution. Current approval status: '{approval_status}'."
            )

        return True
