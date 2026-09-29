"""Isolated State Snapshot Engine for Counterfactual Simulation.

Ensures simulations execute strictly in isolated, read-only memory snapshots
without ever mutating production PostgreSQL state.
"""

import uuid
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import Customer, Event, Decision, Action, Experience
from app.services.memory_service import memory_service
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


class StateSnapshot:
    """Read-only immutable snapshot of organizational state marked SIMULATION_ONLY."""

    def __init__(
        self,
        snapshot_id: str,
        organization_id: str,
        timestamp: str,
        source_request: Optional[str] = None,
        customers: Optional[List[Dict[str, Any]]] = None,
        events: Optional[List[Dict[str, Any]]] = None,
        decisions: Optional[List[Dict[str, Any]]] = None,
        actions: Optional[List[Dict[str, Any]]] = None,
        experiences: Optional[List[Dict[str, Any]]] = None,
        active_risks: Optional[List[Dict[str, Any]]] = None,
        relevant_memories: Optional[List[Dict[str, Any]]] = None,
    ):
        self.snapshot_id = snapshot_id
        self.organization_id = organization_id
        self.timestamp = timestamp
        self.source_request = source_request or "system_simulation_snapshot"
        self.customers = customers or []
        self.events = events or []
        self.decisions = decisions or []
        self.actions = actions or []
        self.experiences = experiences or []
        self.active_risks = active_risks or []
        self.relevant_memories = relevant_memories or []
        self.simulation_tag = "SIMULATION_ONLY"
        self.state_hash = self._compute_state_hash()

    def _compute_state_hash(self) -> str:
        data = {
            "snapshot_id": self.snapshot_id,
            "organization_id": self.organization_id,
            "customer_count": len(self.customers),
            "event_count": len(self.events),
            "experience_count": len(self.experiences),
            "timestamp": self.timestamp,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "organization_id": self.organization_id,
            "timestamp": self.timestamp,
            "source_request": self.source_request,
            "simulation_tag": self.simulation_tag,
            "state_hash": self.state_hash,
            "entities": {
                "customers": self.customers,
                "decisions": self.decisions,
                "actions": self.actions,
            },
            "events": self.events,
            "experiences": self.experiences,
            "active_risks": self.active_risks,
            "relevant_memories": self.relevant_memories,
        }

    @classmethod
    def capture(
        cls,
        db: Session,
        organization_id: uuid.UUID,
        source_request: Optional[str] = None,
        as_of_timestamp: Optional[datetime] = None,
    ) -> "StateSnapshot":
        """Captures an isolated snapshot of organizational state. If as_of_timestamp is provided,

        reconstructs historical state as it existed at that time.
        """
        snap_id = f"snap-{uuid.uuid4().hex[:12]}"
        now_str = (as_of_timestamp or datetime.now(timezone.utc)).isoformat()
        logger.info(f"[SIMULATION_START] Capturing SnapshotID={snap_id} for Org={organization_id} AsOf={now_str}")

        # Query customers
        cust_query = select(Customer).where(Customer.organization_id == organization_id)
        if as_of_timestamp:
            cust_query = cust_query.where(Customer.created_at <= as_of_timestamp)
        customers = [
            {
                "id": str(c.id),
                "name": c.name,
                "risk_level": c.risk_level,
                "status": c.status,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in db.scalars(cust_query).all()
        ]

        # Query events
        ev_query = select(Event).where(Event.organization_id == organization_id)
        if as_of_timestamp:
            ev_query = ev_query.where(Event.created_at <= as_of_timestamp)
        events = [
            {
                "id": str(e.id),
                "title": e.title,
                "event_type": e.event_type,
                "severity": (e.metadata_json or {}).get("severity", "info"),
                "entity_id": e.entity_id,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in db.scalars(ev_query.order_by(Event.created_at.desc()).limit(20)).all()
        ]

        # Query decisions
        dec_query = select(Decision).where(Decision.organization_id == organization_id)
        if as_of_timestamp:
            dec_query = dec_query.where(Decision.created_at <= as_of_timestamp)
        decisions = [
            {
                "id": str(d.id),
                "title": d.title,
                "status": d.status,
                "reasoning": d.reasoning,
            }
            for d in db.scalars(dec_query.limit(10)).all()
        ]

        # Query actions
        act_query = select(Action).where(Action.organization_id == organization_id)
        if as_of_timestamp:
            act_query = act_query.where(Action.created_at <= as_of_timestamp)
        actions = [
            {
                "id": str(a.id),
                "action_type": a.action_type,
                "status": a.status,
                "risk_level": a.risk_level,
                "approval_required": a.approval_required,
            }
            for a in db.scalars(act_query.limit(10)).all()
        ]

        # Query experiences
        exp_query = select(Experience).where(Experience.organization_id == organization_id)
        if as_of_timestamp:
            exp_query = exp_query.where(Experience.created_at <= as_of_timestamp)
        experiences = [
            {
                "id": str(x.id),
                "description": x.description,
                "success": x.success,
                "outcome": x.outcome,
                "created_at": x.created_at.isoformat() if x.created_at else None,
            }
            for x in db.scalars(exp_query.limit(10)).all()
        ]

        # Synthesize active risks
        active_risks = []
        for c in customers:
            if c.get("risk_level") == "high":
                active_risks.append({
                    "risk_type": "customer_churn",
                    "entity": c["name"],
                    "severity": "high",
                    "description": f"Customer {c['name']} has flagged high risk status.",
                })

        # Query Hindsight memory snapshot
        relevant_memories = []
        try:
            query_term = source_request or "operational payment incident failure"
            h_mems = memory_service.recall_memories(
                query=query_term,
                bank_id=settings.HINDSIGHT_BANK_ID,
                max_tokens=2048,
            )
            for m in h_mems:
                relevant_memories.append({
                    "text": m.get("text"),
                    "tags": m.get("tags", []),
                })
        except Exception as e:
            logger.warning(f"State snapshot Hindsight query notice: {e}")

        return cls(
            snapshot_id=snap_id,
            organization_id=str(organization_id),
            timestamp=now_str,
            source_request=source_request,
            customers=customers,
            events=events,
            decisions=decisions,
            actions=actions,
            experiences=experiences,
            active_risks=active_risks,
            relevant_memories=relevant_memories,
        )
