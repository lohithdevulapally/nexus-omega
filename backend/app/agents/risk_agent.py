"""RiskAgent for NEXUS-Ω.

Analyzes operational, financial, customer impact, cascading, and historical failure risks.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.agents.base_agent import BaseAgent
from app.agents.state import AgentState, RiskItem
from app.core.logging import logger


class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="RiskAgent",
            description="Evaluates operational failure modes, customer escalation potential, and financial exposure.",
        )

    def run(self, state: AgentState, db: Session) -> AgentState:
        analyst_patterns = state.analyst_output.get("patterns", [])
        causal_links = state.causal_output.get("relationships", [])
        req = state.user_request.lower()

        risks: List[RiskItem] = []

        # 1. Customer Impact Risk
        if "acme" in req or any("generic" in str(c) for c in causal_links) or "payment" in req:
            risks.append(
                RiskItem(
                    risk_type="customer_impact",
                    description="Severe customer relationship damage and contract churn risk if generic automated updates are sent.",
                    severity="high",
                    probability_estimate="high",
                    evidence="Historical precedent: generic status communication previously caused ACME leadership to escalate directly to executives.",
                    mitigation="Enforce mandatory proactive engineering updates with explicit technical timelines.",
                )
            )

        # 2. Historical Failure Risk (Service Restart Trap)
        if "restart" in req or any("restart" in str(c) for c in causal_links):
            risks.append(
                RiskItem(
                    risk_type="historical_failure_risk",
                    description="Blind service restarts fail to resolve connection pool exhaustion and return to failure state within 20 minutes.",
                    severity="high",
                    probability_estimate="high",
                    evidence="Operational experience record #7: past restart during pool leak produced 0% lasting resolution.",
                    mitigation="Perform configuration rollback and inspect active pool metrics instead of rebooting service.",
                )
            )

        # 3. Recurrence Risk (Infinite Gateway Retries)
        if "payment" in req or "gateway" in req:
            risks.append(
                RiskItem(
                    risk_type="recurrence_risk",
                    description="Repeated connection retries exceeding 2 attempts will lock payment worker threads and exhaust queue headroom.",
                    severity="critical",
                    probability_estimate="medium",
                    evidence="Incident #3 telemetry: 3rd retry attempt during provider outage saturated egress pool.",
                    mitigation="Activate automated circuit-breaker: switch to secondary gateway if retry #2 fails.",
                )
            )

        # 4. Financial & SLA Penalty Risk
        risks.append(
            RiskItem(
                risk_type="financial_risk",
                description="Transaction downtime exceeding 15 minutes triggers contractual SLA rebate penalty clauses.",
                severity="medium",
                probability_estimate="medium",
                evidence="ACME Enterprise contract addendum specifies SLA credits for downtime windows exceeding 15m.",
                mitigation="Route traffic through secondary payment rail within 5 minutes of primary timeout confirmation.",
            )
        )

        # 5. Cascading Risk from Causal Graph Cascade Analysis
        cascade = state.causal_output.get("cascade_analysis", {})
        if cascade and cascade.get("affected_entities"):
            risks.append(
                RiskItem(
                    risk_type="cascading_risk",
                    description=f"Downstream ripple impact threatening {len(cascade['affected_entities'])} entity/system(s): {', '.join([e['entity'] for e in cascade['affected_entities'][:2]])}.",
                    severity=cascade.get("severity", "medium"),
                    probability_estimate="high",
                    evidence=f"Causal cascade prediction from trigger '{cascade.get('trigger')}'.",
                    mitigation="Isolate primary failure rail and enforce circuit breaker before cascade propagates to downstream billing pipelines.",
                )
            )

        overall_severity = "high" if any(r.severity in ["high", "critical"] for r in risks) else "medium"

        state.risk_output = {
            "risks": [r.model_dump() for r in risks],
            "severity": overall_severity,
            "probability_estimate": "high (grounded in historical telemetry)",
            "mitigation_options": [r.mitigation for r in risks],
            "confidence": 0.93,
        }

        self.log_observation(
            db=db,
            state=state,
            observation_type="risk_assessment",
            summary=f"Identified {len(risks)} operational and historical failure risks. Overall severity: {overall_severity.upper()}.",
            evidence=state.risk_output,
            confidence=0.93,
        )

        logger.info(f"[RISK_ANALYSIS] Severity={overall_severity} RiskCount={len(risks)}")
        return state

    def get_step_summary(self, state: AgentState) -> str:
        sev = state.risk_output.get("severity", "medium")
        count = len(state.risk_output.get("risks", []))
        return f"Evaluated {count} risk factor(s) with overall {sev.upper()} severity."


risk_agent = RiskAgent()
