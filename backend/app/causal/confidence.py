"""Nuanced Causal Confidence Engine.

Ensures correlation is strictly differentiated from causation, weighting confidence by
empirical evidence counts, Hindsight episodic memory citations, and counter-evidence penalties.
"""

from typing import Dict, Any, List


class CausalConfidenceCalculator:
    RELATIONSHIP_PRIORS = {
        "CAUSES": 0.80,
        "RESULTED_IN": 0.90,
        "RESOLVED_BY": 0.90,
        "FAILED_BECAUSE_OF": 0.88,
        "TRIGGERS": 0.82,
        "CONTRIBUTES_TO": 0.75,
        "DEPENDS_ON": 0.85,
        "AMPLIFIES": 0.78,
        "MITIGATES": 0.82,
        "PRECEDED": 0.65,
        "FOLLOWED_BY": 0.65,
        "CORRELATED_WITH": 0.50,  # Never treat correlation as causation!
        "CONTRADICTS": 0.80,
    }

    @classmethod
    def calculate_confidence(
        cls,
        relationship: str,
        supporting_events: List[Any],
        supporting_memories: List[Any],
        counter_evidence: List[Any],
        base_confidence: float = None,
    ) -> float:
        """Calculates grounded causal confidence score between 0.0 and 1.0."""
        # 1. Base prior
        score = base_confidence if base_confidence is not None else cls.RELATIONSHIP_PRIORS.get(relationship, 0.70)

        # 2. Correlated with cannot exceed 0.65 without direct intervention evidence
        if relationship == "CORRELATED_WITH":
            return min(score + (len(supporting_events) * 0.02), 0.65)

        # 3. Additive evidence boosts
        event_boost = min(len(supporting_events) * 0.04, 0.15)
        memory_boost = min(len(supporting_memories) * 0.05, 0.18)
        score += (event_boost + memory_boost)

        # 4. Counter-evidence penalty
        if counter_evidence:
            penalty = len(counter_evidence) * 0.15
            score -= penalty

        # Clamp between 0.10 and 0.99 (true certainty in complex organizations is non-trivial)
        return max(0.10, min(0.99, round(score, 3)))
