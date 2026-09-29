"""Scenario generators for deterministic counterfactual simulations."""

from typing import List, Dict, Any, Optional
from app.simulation.simulation_models import CounterfactualScenario
from app.simulation.state_snapshot import StateSnapshot


class ScenarioBuilder:
    """Constructs structured baseline vs alternative scenarios grounded in snapshot state."""

    @staticmethod
    def build_counterfactual_scenario(
        baseline_action: str,
        alternative_action: str,
        snapshot: StateSnapshot,
        incident_context: str = "payment gateway degradation",
    ) -> CounterfactualScenario:
        """Constructs an explicit comparison scenario between a chosen baseline action

        and an alternative what-if action.
        """
        assumptions = [
            f"Active incident '{incident_context}' continues without organic self-recovery.",
            "Incoming transactional traffic volume remains at normal operational baseline.",
            "Underlying network routing rules remain deterministic during intervention window.",
        ]

        constraints = [
            "Contractual SLA allows maximum 15 minutes before financial credit penalties trigger.",
            "Service restart introduces 90-second cold-start connection blackout.",
            "Secondary rail B capacity is capped at 120% of peak ACME transaction volume.",
        ]

        # Gather relevant historical analogues from snapshot memories
        historical_evidence = []
        for mem in snapshot.relevant_memories:
            txt = mem.get("text", "")
            if any(term in txt.lower() for term in ["restart", "switch", "rail", "gateway", "incident"]):
                historical_evidence.append({
                    "evidence": txt,
                    "source": "Hindsight Memory Snapshot",
                })

        return CounterfactualScenario(
            name=f"Comparison: {baseline_action} vs {alternative_action}",
            description=f"Evaluating operational divergence between '{baseline_action}' and '{alternative_action}' under incident conditions.",
            baseline_action=baseline_action,
            alternative_action=alternative_action,
            assumptions=assumptions,
            constraints=constraints,
            starting_state={
                "snapshot_id": snapshot.snapshot_id,
                "customer_count": len(snapshot.customers),
                "active_risks_count": len(snapshot.active_risks),
                "timestamp": snapshot.timestamp,
            },
            historical_evidence=historical_evidence,
        )
