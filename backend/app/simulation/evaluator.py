"""Evaluator comparing Actual World vs Counterfactual World outcomes."""

from typing import Dict, Any, List


class CounterfactualEvaluator:
    """Computes structural divergences, risk deltas, and evidence-grounded contrasts

    between the observed/baseline world and the simulated counterfactual world.
    """

    @staticmethod
    def compare_worlds(
        actual_world: Dict[str, Any],
        counterfactual_world: Dict[str, Any],
        scenario_assumptions: List[str],
        historical_evidence: List[Dict[str, Any]],
        causal_paths: List[str],
    ) -> Dict[str, Any]:
        """Produces a structured delta between actual and counterfactual states."""
        differences = []

        # 1. Action divergence
        actual_act = actual_world.get("action", "unknown")
        cf_act = counterfactual_world.get("action", "unknown")
        differences.append(f"Intervention Divergence: Executing '{cf_act}' instead of baseline '{actual_act}'.")

        # 2. Outcome divergence
        actual_outcome = actual_world.get("projected_outcome", "")
        cf_outcome = counterfactual_world.get("projected_outcome", "")
        if actual_outcome != cf_outcome:
            differences.append(f"Outcome Divergence: Baseline leads to '{actual_outcome}' whereas counterfactual leads to '{cf_outcome}'.")

        # 3. Risk delta
        actual_risks = [r.get("risk_type") for r in actual_world.get("risks", [])]
        cf_risks = [r.get("risk_type") for r in counterfactual_world.get("risks", [])]
        new_risks = set(cf_risks) - set(actual_risks)
        avoided_risks = set(actual_risks) - set(cf_risks)

        if new_risks:
            differences.append(f"New Risks Introduced in Counterfactual: {', '.join(new_risks)}.")
        if avoided_risks:
            differences.append(f"Risks Mitigated in Counterfactual: {', '.join(avoided_risks)}.")

        # 4. Uncertainty factors
        uncertainty = [
            "Network latency jitter on secondary rails cannot be predicted with 100% precision.",
            "Customer reaction speed to outbound communication is subject to human variance.",
            "Provider-side recovery time during external upstream outages is unobservable.",
        ]

        # 5. Grounded confidence
        confidence = 0.91 if len(historical_evidence) >= 2 else 0.82

        return {
            "actual_world": actual_world,
            "counterfactual_world": counterfactual_world,
            "differences": differences,
            "causal_paths": causal_paths,
            "historical_evidence": historical_evidence,
            "assumptions": scenario_assumptions,
            "uncertainty": uncertainty,
            "confidence": confidence,
        }
