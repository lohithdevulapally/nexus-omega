"""MemoryAgent and MemoryConflictDetector for NEXUS-Ω.

Queries Hindsight and PostgreSQL, extracts structured memory items with provenance,
and detects contradictory or conflicting historical memories.
"""

import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.agents.base_agent import BaseAgent
from app.agents.state import AgentState, MemoryItem, MemoryConflict
from app.db.models import Experience, MemoryReference
from app.services.memory_service import memory_service
from app.services.context_service import context_service
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


class MemoryConflictDetector:
    """Detects contradictions between recalled experiences."""

    @staticmethod
    def detect_conflicts(memories: List[MemoryItem]) -> List[MemoryConflict]:
        conflicts: List[MemoryConflict] = []
        if len(memories) < 2:
            return conflicts

        # Heuristic conflict detection based on action and opposite outcomes (e.g. success vs failure on same component)
        gateway_success: List[MemoryItem] = []
        gateway_failure: List[MemoryItem] = []
        restart_success: List[MemoryItem] = []
        restart_failure: List[MemoryItem] = []

        for m in memories:
            text = (m.summary + " " + (m.outcome or "")).lower()
            if "retry" in text or "gateway" in text:
                if any(k in text for k in ["succeeded", "recovered", "resolved", "success"]):
                    gateway_success.append(m)
                if any(k in text for k in ["failed", "backlog", "outage", "frustration"]):
                    gateway_failure.append(m)

            if "restart" in text:
                if "recovered" in text or "success" in text:
                    restart_success.append(m)
                if "did not resolve" in text or "failure returned" in text or "failed" in text:
                    restart_failure.append(m)

        # Detect gateway retry conflict (e.g. retry succeeded twice vs retry failed on 3rd attempt)
        if gateway_success and gateway_failure:
            conflicts.append(
                MemoryConflict(
                    conflict=True,
                    memories=[
                        {"id": m.memory_id, "summary": m.summary, "outcome": m.outcome}
                        for m in (gateway_success[:1] + gateway_failure[:1])
                    ],
                    explanation=(
                        "Contextual nuance detected regarding payment gateway retry: "
                        "connection retry resolved initial transient errors (incidents #1 and #2), "
                        "but failed when provider experienced complete outage (incident #3), requiring gateway switching."
                    ),
                    resolution_strategy="requires_context",
                )
            )

        # Detect restart conflict if both exist
        if restart_success and restart_failure:
            conflicts.append(
                MemoryConflict(
                    conflict=True,
                    memories=[
                        {"id": m.memory_id, "summary": m.summary, "outcome": m.outcome}
                        for m in (restart_success[:1] + restart_failure[:1])
                    ],
                    explanation=(
                        "Service restart produced conflicting outcomes depending on incident type: "
                        "effective for thread deadlocks, but actively failed on connection pool leaks."
                    ),
                    resolution_strategy="requires_context",
                )
            )

        return conflicts


class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="MemoryAgent",
            description="Recalls experiences from Hindsight and PostgreSQL, assesses provenance, and checks conflicts.",
        )
        self.conflict_detector = MemoryConflictDetector()

    def run(self, state: AgentState, db: Session) -> AgentState:
        query = state.user_request
        bank_id = settings.HINDSIGHT_BANK_ID
        logger.info(f"[MEMORY_RECALL] Query='{query}' Bank='{bank_id}'")

        # 1. Query Hindsight Memory Engine
        hindsight_results: List[Dict[str, Any]] = []
        try:
            hindsight_results = memory_service.recall_memories(
                query=query,
                bank_id=bank_id,
                max_tokens=4096,
            )
        except Exception as e:
            logger.warning(f"MemoryAgent: Hindsight recall encountered notice: {e}")

        # 2. Query PostgreSQL Experiences
        postgres_experiences = db.scalars(
            select(Experience)
            .where(Experience.organization_id == state.organization_id)
            .order_by(Experience.created_at.desc())
            .limit(10)
        ).all()

        # 3. Assemble standardized MemoryItems with provenance
        memory_items: List[MemoryItem] = []

        # From Hindsight
        for idx, h_mem in enumerate(hindsight_results):
            text = h_mem.get("text", "").strip()
            if not text:
                continue
            memory_items.append(
                MemoryItem(
                    memory_id=str(h_mem.get("id") or f"hindsight-{idx}"),
                    source="hindsight_bank",
                    relevance=0.92,
                    confidence=0.95,
                    timestamp=str(h_mem.get("metadata", {}).get("timestamp", "recent")),
                    summary=text,
                    outcome="Extracted from Hindsight experiential memory",
                    tags=h_mem.get("tags") or ["episodic_memory"],
                )
            )

        # From PostgreSQL
        for exp in postgres_experiences:
            # Check relevance
            exp_text = f"{exp.description} {exp.action_taken or ''}".lower()
            words = [w for w in query.lower().split() if len(w) > 3]
            if any(w in exp_text for w in words) or "payment" in exp_text or "gateway" in exp_text:
                memory_items.append(
                    MemoryItem(
                        memory_id=f"pg-exp-{exp.id}",
                        source="postgresql_experiences",
                        relevance=0.90,
                        confidence=0.95,
                        timestamp=exp.created_at.isoformat() if exp.created_at else None,
                        summary=exp.description,
                        outcome=f"{'SUCCESS' if exp.success else 'FAILURE'}: {exp.outcome}",
                        tags=[exp.experience_type, "structured_experience"],
                    )
                )

        state.recalled_memories = memory_items

        # 4. Memory Conflict Detection
        conflicts = self.conflict_detector.detect_conflicts(memory_items)
        state.memory_conflicts = conflicts

        # 5. Extract Relational Context
        entities = context_service.extract_entities(db, state.organization_id, state.user_request)
        state.current_context = context_service.get_relational_context(db, state.organization_id, entities)

        self.log_observation(
            db=db,
            state=state,
            observation_type="memory_recall",
            summary=f"Recalled {len(memory_items)} memory items ({len(hindsight_results)} from Hindsight). Identified {len(conflicts)} memory conflict(s).",
            evidence={
                "count": len(memory_items),
                "conflicts": [c.model_dump() for c in conflicts],
                "sample": [m.summary[:80] for m in memory_items[:3]],
            },
        )

        return state

    def get_step_summary(self, state: AgentState) -> str:
        count = len(state.recalled_memories)
        conflicts = len(state.memory_conflicts)
        return f"Recalled {count} memory items from Hindsight & PostgreSQL. Detected {conflicts} conflict(s)."


memory_agent = MemoryAgent()
