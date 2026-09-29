"""Multi-Agent Orchestrator for NEXUS-Ω.

Executes the sequential and conditional agent graph:
Planner -> Memory -> Analyst -> Causal -> Risk -> Decision -> Critic -> Human Approval Check -> Reflection
"""

import time
import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.agents.state import AgentState
from app.agents.planner_agent import planner_agent
from app.agents.memory_agent import memory_agent
from app.agents.analyst_agent import analyst_agent
from app.agents.causal_agent import causal_agent
from app.agents.risk_agent import risk_agent
from app.agents.decision_agent import decision_agent
from app.agents.critic_agent import critic_agent
from app.agents.reflection_agent import reflection_agent
from app.core.logging import logger


class AgentOrchestrator:
    def __init__(self):
        # Graph nodes
        self.planner = planner_agent
        self.memory = memory_agent
        self.analyst = analyst_agent
        self.causal = causal_agent
        self.risk = risk_agent
        self.decision = decision_agent
        self.critic = critic_agent
        self.reflection = reflection_agent

    def run_investigation(
        self,
        db: Session,
        organization_id: uuid.UUID,
        user_request: str,
        user_id: Optional[str] = None,
        auto_reflect: bool = True,
    ) -> AgentState:
        """Runs the complete multi-agent investigation and decision graph."""
        req_id = str(uuid.uuid4())
        logger.info(f"[ORCHESTRATOR_START] RequestID={req_id} Request='{user_request[:80]}...'")

        # Initialize shared agent state
        state = AgentState(
            request_id=req_id,
            organization_id=organization_id,
            user_id=user_id,
            user_request=user_request,
            status="planning",
        )

        # Node 1: Planner
        state = self.planner.execute(state, db)

        # Node 2: Memory (Hindsight + PostgreSQL)
        state.status = "remembering"
        state = self.memory.execute(state, db)

        # Node 3: Analyst (State + Memory Synthesis)
        state.status = "analyzing"
        state = self.analyst.execute(state, db)

        # Node 4: Causal Reasoning
        state.status = "causal_reasoning"
        state = self.causal.execute(state, db)

        # Node 5: Decision Formulation & Counterfactual Simulation
        state.status = "deciding_and_simulating"
        state = self.decision.execute(state, db)

        # Node 6: Risk Assessment (incorporates simulation & cascade risks)
        state.status = "assessing_risk"
        state = self.risk.execute(state, db)

        # Node 7: Adversarial Critic (attacks decisions and simulation assumptions)
        state.status = "critiquing"
        state = self.critic.execute(state, db)

        # Node 8: Simulated Execution & Post-Action Reflection
        if auto_reflect:
            state.status = "reflecting"
            state = self.reflection.execute(state, db)

        state.status = "completed"
        state.timestamps["completed_at"] = datetime.now(timezone.utc).isoformat()
        logger.info(f"[ORCHESTRATOR_COMPLETE] RequestID={req_id} StepsCompleted={len(state.timeline)}")
        return state


orchestrator = AgentOrchestrator()
