"""PlannerAgent for NEXUS-Ω.

Deconstructs complex user requests into structured, executable subtasks and identifies required agent capabilities.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.agents.base_agent import BaseAgent
from app.agents.state import AgentState
from app.services.context_service import context_service
from app.core.logging import logger


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="PlannerAgent",
            description="Decomposes user requests into structured subtasks, identifying data and agent requirements.",
        )

    def run(self, state: AgentState, db: Session) -> AgentState:
        req = state.user_request.lower()

        # Step 1: Extract entities and intent using ContextService
        entities = context_service.extract_entities(db, state.organization_id, state.user_request)
        classification = context_service.classify_message(state.user_request)

        # Step 2: Formulate dynamic execution steps based on context
        plan_steps: List[str] = [
            "1. Retrieve current relational entity state from PostgreSQL",
            "2. Recall episodic experiences and operational resolutions from Hindsight",
            "3. Synthesize operational findings, comparative patterns, and anomalies",
            "4. Map causal relationships and historical dependency chains",
            "5. Evaluate recurrence, operational, and customer impact risks",
            "6. Formulate high-confidence candidate decisions",
            "7. Perform adversarial critique and anti-failure verification",
            "8. Determine human approval requirement and assemble actionable recommendation",
            "9. Prepare post-action reflection and Hindsight retention pipeline",
        ]

        required_data = [
            f"Customer profile ({', '.join(entities.get('customer_names', [])) or 'General'})",
            "Recent service incidents and open tickets",
            "Operational deployment history",
        ]

        required_memories = [
            "Historical incident resolutions",
            "Customer-specific communication preferences",
            "Known operational anti-patterns and failure outcomes",
        ]

        required_agents = [
            "MemoryAgent",
            "AnalystAgent",
            "CausalAgent",
            "RiskAgent",
            "DecisionAgent",
            "CriticAgent",
            "ReflectionAgent",
        ]

        state.planner_output = {
            "objective": state.user_request,
            "classification": classification,
            "entities_identified": entities,
            "plan_steps": plan_steps,
            "required_data": required_data,
            "required_memories": required_memories,
            "required_agents": required_agents,
            "confidence": 0.95,
        }

        self.log_observation(
            db=db,
            state=state,
            observation_type="execution_plan",
            summary=f"Formulated {len(plan_steps)}-step execution plan across {len(required_agents)} specialized agents.",
            evidence={"plan": plan_steps, "classification": classification},
        )

        return state

    def get_step_summary(self, state: AgentState) -> str:
        steps = state.planner_output.get("plan_steps", [])
        return f"Formulated {len(steps)}-step execution plan addressing request."


planner_agent = PlannerAgent()
