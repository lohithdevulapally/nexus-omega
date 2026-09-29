"""Action Registry defining safe, controlled operational interventions.

Strictly prohibits arbitrary shell commands or unrestricted external HTTP calls.
"""

from enum import Enum
from typing import Dict, Any, List, Set


class ActionType(str, Enum):
    CREATE_INTERNAL_EVENT = "create_internal_event"
    UPDATE_CUSTOMER_STATUS = "update_customer_status"
    CREATE_INCIDENT = "create_incident"
    SEND_WEBHOOK = "send_webhook"
    CREATE_NOTIFICATION = "create_notification"
    SIMULATE_ACTION = "simulate_action"
    SWITCH_PAYMENT_RAIL = "switch_payment_rail"


class ActionRiskTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ActionRegistry:
    """Whitelisted action specifications, parameter schemas, and risk tiers."""

    ACTION_METADATA: Dict[str, Dict[str, Any]] = {
        ActionType.CREATE_INTERNAL_EVENT.value: {
            "risk_tier": ActionRiskTier.LOW.value,
            "requires_human_approval": False,
            "required_parameters": ["title", "event_type"],
            "allowed_parameters": ["title", "event_type", "severity", "entity_id", "metadata"],
            "description": "Appends an operational event into the PostgreSQL events log.",
        },
        ActionType.CREATE_NOTIFICATION.value: {
            "risk_tier": ActionRiskTier.LOW.value,
            "requires_human_approval": False,
            "required_parameters": ["recipient", "message"],
            "allowed_parameters": ["recipient", "message", "channel", "priority"],
            "description": "Dispatches an internal alert/notification to ops or engineering teams.",
        },
        ActionType.SIMULATE_ACTION.value: {
            "risk_tier": ActionRiskTier.LOW.value,
            "requires_human_approval": False,
            "required_parameters": ["simulated_action"],
            "allowed_parameters": ["simulated_action", "context", "parameters"],
            "description": "Performs an in-memory test execution without modifying persistent state.",
        },
        ActionType.UPDATE_CUSTOMER_STATUS.value: {
            "risk_tier": ActionRiskTier.MEDIUM.value,
            "requires_human_approval": True,
            "required_parameters": ["customer_id"],
            "allowed_parameters": ["customer_id", "status", "risk_level", "reason"],
            "description": "Modifies customer operational standing or account risk level in PostgreSQL.",
        },
        ActionType.CREATE_INCIDENT.value: {
            "risk_tier": ActionRiskTier.MEDIUM.value,
            "requires_human_approval": True,
            "required_parameters": ["title", "severity"],
            "allowed_parameters": ["title", "severity", "entity_id", "description"],
            "description": "Escalates an operational failure into a tracked enterprise incident.",
        },
        ActionType.SEND_WEBHOOK.value: {
            "risk_tier": ActionRiskTier.HIGH.value,
            "requires_human_approval": True,
            "required_parameters": ["endpoint_url", "payload"],
            "allowed_parameters": ["endpoint_url", "payload", "headers", "method"],
            "description": "Transmits an outbound webhook payload to an integrated third-party system.",
        },
        ActionType.SWITCH_PAYMENT_RAIL.value: {
            "risk_tier": ActionRiskTier.HIGH.value,
            "requires_human_approval": True,
            "required_parameters": ["from_rail", "to_rail"],
            "allowed_parameters": ["from_rail", "to_rail", "drain_timeout_sec", "reason", "status"],
            "description": "Reroutes transaction traffic from primary degraded rail to secondary standby rail.",
        },
    }

    @classmethod
    def get_action_spec(cls, action_type: str) -> Dict[str, Any]:
        spec = cls.ACTION_METADATA.get(action_type)
        if not spec:
            raise ValueError(f"Action '{action_type}' is not registered or permitted in NEXUS-Ω ActionRegistry.")
        return spec

    @classmethod
    def is_registered(cls, action_type: str) -> bool:
        return action_type in cls.ACTION_METADATA
