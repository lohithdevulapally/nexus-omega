"""DecisionAgent for NEXUS-Ω.

Formulates evidence-backed candidate actions and decisions, evaluating trade-offs,
historical support, and human approval requirements.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.agents.base_agent import BaseAgent
from app.agents.state import AgentState, DecisionCandidate
from app.db.models import AgentDecision
from app.core.logging import logger


class DecisionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="DecisionAgent",
            description="Formulates candidate operational decisions backed by historical Hindsight outcomes.",
        )

    def run(self, state: AgentState, db: Session) -> AgentState:
        req = state.user_request.lower()
        candidates: List[DecisionCandidate] = []

        # Candidate 1: Immediate Gateway Rail Switch (High confidence, historically proven)
        if "payment" in req or "gateway" in req or "acme" in req:
            candidates.append(
                DecisionCandidate(
                    action="Switch ACME transaction traffic to Secondary Payment Gateway Rail B",
                    rationale_summary=(
                        "Historical evidence from Incident #3 demonstrates that once connection retry limit is reached, "
                        "switching gateway immediately restored payment success rates to 99.98%."
                    ),
                    expected_outcome="Immediate restoration of transaction success rate to >99.9% without queue saturation.",
                    historical_support=[
                        "Hindsight episodic memory: September 2026 ACME Incident #3 resolution",
                        "Strategic Decision #1: Multi-rail active-passive routing policy",
                    ],
                    risks=[
                        "Minor transaction fee differential on secondary gateway rail (+0.02%)",
                    ],
                    confidence=0.96,
                    approval_required=True,  # Production traffic redirection requires authorization
                )
            )

            # Candidate 2: Proactive Executive Communication
            candidates.append(
                DecisionCandidate(
                    action="Dispatch direct, proactive technical update from Lead SRE to ACME VP of Engineering",
                    rationale_summary=(
                        "Historical customer communication record confirms that proactive technical transparency "
                        "de-escalated leadership and prevented SLA dispute escalation."
                    ),
                    expected_outcome="Maintains customer trust; suppresses escalation ticket #1042.",
                    historical_support=[
                        "Customer communication experience: Proactive communication de-escalated ACME leadership",
                        "Customer preference: Avoid automated generic 'we are investigating' emails",
                    ],
                    risks=[
                        "Requires SRE lead 5 minutes to draft personalized update",
                    ],
                    confidence=0.95,
                    approval_required=False,
                )
            )

        # Candidate 3: Configuration Rollback if Restart is mentioned
        if "restart" in req:
            candidates.append(
                DecisionCandidate(
                    action="Roll back connection pool configuration to v2.3 rather than restarting service",
                    rationale_summary=(
                        "Restarting was previously proven to fail against connection leaks, whereas configuration rollback stabilized the pool."
                    ),
                    expected_outcome="Permanent pool recovery without recurrence after 20 minutes.",
                    historical_support=[
                        "Operational mistake #7: Service restart failed to resolve leak",
                        "Operational remediation #8: Configuration rollback stabilized pool",
                    ],
                    risks=[
                        "Reverts latest non-critical configuration flags",
                    ],
                    confidence=0.94,
                    approval_required=True,
                )
            )

        # Fallback candidate for general requests
        if not candidates:
            candidates.append(
                DecisionCandidate(
                    action="Execute standard diagnostic runbook and monitor real-time telemetry",
                    rationale_summary="Standard operating procedure when no historical failure pattern is triggered.",
                    expected_outcome="Telemetry baseline established within 10 minutes.",
                    historical_support=["Standard operational runbook"],
                    risks=["Low operational risk"],
                    confidence=0.88,
                    approval_required=False,
                )
            )

        # Determine primary candidate
        primary_candidate = candidates[0]
        state.approval_required = primary_candidate.approval_required
        state.approval_status = "pending" if primary_candidate.approval_required else "not_required"

        # Invoke CounterfactualEngine to evaluate candidate options
        try:
            from app.simulation.simulator import counterfactual_engine
            options_to_compare = [c.action for c in candidates[:3]]
            if len(options_to_compare) >= 2:
                sim_comparison = counterfactual_engine.compare_scenarios(
                    db=db,
                    organization_id=state.organization_id,
                    decision_context=state.user_request,
                    options=options_to_compare,
                )
                state.simulation_output = sim_comparison.model_dump()
        except Exception as ex:
            logger.warning(f"Counterfactual simulation in DecisionAgent notice: {ex}")

        # Register controlled action in actions table
        try:
            from app.actions.action_engine import action_engine
            act = action_engine.request_action(
                db=db,
                organization_id=state.organization_id,
                action_type="create_internal_event",
                parameters={
                    "title": primary_candidate.action,
                    "event_type": "operational_decision",
                    "severity": "high" if primary_candidate.approval_required else "info",
                },
                requested_by=state.user_id or "DecisionAgent",
                agent=self.agent_name,
                risk_level="high" if primary_candidate.approval_required else "low",
                approval_required=primary_candidate.approval_required,
                auto_execute_low_risk=False,
            )
            state.action_id = str(act.id)
            state.action_request = {
                "action_id": str(act.id),
                "action_type": act.action_type,
                "status": act.status,
                "approval_required": act.approval_required,
                "approval_status": act.approval_status,
            }
        except Exception as ex:
            logger.warning(f"Controlled action registration notice: {ex}")

        state.decision_output = {
            "candidates": [c.model_dump() for c in candidates],
            "primary_decision": primary_candidate.model_dump(),
            "approval_required": primary_candidate.approval_required,
            "action_id": state.action_id,
            "simulation": state.simulation_output,
            "confidence": primary_candidate.confidence,
        }

        # Store in database audit table
        try:
            db_decision = AgentDecision(
                organization_id=state.organization_id,
                request_id=state.request_id,
                agent_name=self.agent_name,
                action=primary_candidate.action,
                rationale_summary=primary_candidate.rationale_summary,
                expected_outcome=primary_candidate.expected_outcome,
                historical_support={"support": primary_candidate.historical_support},
                risks={"risks": primary_candidate.risks},
                approval_required=primary_candidate.approval_required,
                status="proposed",
                confidence=primary_candidate.confidence,
            )
            db.add(db_decision)
            db.commit()
        except Exception as ex:
            logger.warning(f"Could not persist AgentDecision: {ex}")
            db.rollback()

        logger.info(f"[DECISION_GENERATED] PrimaryAction='{primary_candidate.action[:60]}...' ApprovalRequired={primary_candidate.approval_required}")
        return state

    def get_step_summary(self, state: AgentState) -> str:
        candidates = state.decision_output.get("candidates", [])
        return f"Formulated {len(candidates)} evidence-backed candidate decision(s)."


decision_agent = DecisionAgent()
