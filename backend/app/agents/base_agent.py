"""BaseAgent abstraction for NEXUS-Ω multi-agent intelligence system."""

import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.agents.state import AgentState, TimelineStep
from app.db.models import AgentObservation, AgentRun
from app.core.logging import logger


class BaseAgent(ABC):
    def __init__(self, agent_name: str, description: str):
        self.agent_name = agent_name
        self.description = description

    @abstractmethod
    def run(self, state: AgentState, db: Session) -> AgentState:
        """Internal execution logic to be implemented by each specialized agent."""
        pass

    def execute(self, state: AgentState, db: Session) -> AgentState:
        """Wraps execution with structured timing, audit logs, and timeline updates."""
        step_num = len(state.timeline) + 1
        logger.info(f"[AGENT_START] Agent={self.agent_name} RequestID={state.request_id} Step={step_num}")
        start_time = time.perf_counter()
        memories_before = len(state.recalled_memories)

        try:
            state = self.run(state, db)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            memories_used = len(state.recalled_memories) - memories_before
            if memories_used < 0:
                memories_used = 0

            step = TimelineStep(
                step=step_num,
                agent=self.agent_name,
                status="completed",
                duration_ms=duration_ms,
                memories_used=memories_used,
                summary=self.get_step_summary(state),
            )
            state.timeline.append(step)

            # Persist an auditable AgentRun record in PostgreSQL
            self._record_audit_run(db, state, duration_ms, status="completed")
            logger.info(f"[{self.agent_name.upper()}_COMPLETE] Duration={duration_ms}ms")
            return state

        except Exception as e:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            err_msg = f"{self.agent_name} failed: {str(e)}"
            logger.error(f"[{self.agent_name.upper()}_ERROR] {err_msg}", exc_info=True)
            state.errors.append(err_msg)
            step = TimelineStep(
                step=step_num,
                agent=self.agent_name,
                status="failed",
                duration_ms=duration_ms,
                memories_used=0,
                summary=err_msg,
            )
            state.timeline.append(step)
            self._record_audit_run(db, state, duration_ms, status="failed", error=err_msg)
            return state

    def get_step_summary(self, state: AgentState) -> str:
        """Provides a concise, auditable reasoning summary for the step without raw private chain-of-thought."""
        return f"{self.agent_name} completed successfully."

    def log_observation(
        self,
        db: Session,
        state: AgentState,
        observation_type: str,
        summary: str,
        evidence: Optional[Dict[str, Any]] = None,
        confidence: float = 0.9,
    ) -> None:
        """Stores a structured auditable observation in PostgreSQL."""
        try:
            obs = AgentObservation(
                organization_id=state.organization_id,
                request_id=state.request_id,
                agent_name=self.agent_name,
                observation_type=observation_type,
                summary=summary,
                evidence_json=evidence or {},
                confidence=confidence,
            )
            db.add(obs)
            db.commit()
        except Exception as ex:
            logger.warning(f"Could not persist AgentObservation: {ex}")
            db.rollback()

    def _record_audit_run(
        self,
        db: Session,
        state: AgentState,
        duration_ms: float,
        status: str,
        error: Optional[str] = None,
    ) -> None:
        """Logs an agent execution run in PostgreSQL."""
        try:
            run = AgentRun(
                organization_id=state.organization_id,
                agent_name=self.agent_name,
                task=f"Execution for request {state.request_id}",
                status=status,
                input_data={"request": state.user_request[:200]},
                output_data={"duration_ms": duration_ms, "error": error} if error else {"duration_ms": duration_ms},
            )
            db.add(run)
            db.commit()
        except Exception as ex:
            logger.warning(f"Could not persist AgentRun: {ex}")
            db.rollback()
