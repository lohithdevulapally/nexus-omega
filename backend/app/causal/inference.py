"""Causal Inference Engine for Path Traversal, Root Cause Analysis, and Cascade Prediction."""

from typing import Dict, Any, List, Optional
from app.causal.graph import CausalKnowledgeGraph
from app.core.logging import logger


class CausalInferenceEngine:
    """Performs rigorous causal inference distinguishing root causes, contributing factors,

    symptoms, and downstream cascades.
    """

    @classmethod
    def find_paths(
        cls, graph: CausalKnowledgeGraph, source: str, target: str, max_depth: int = 5
    ) -> Dict[str, Any]:
        """Discovers strongest causal paths between two entities."""
        src_node = graph.find_node(source)
        tgt_node = graph.find_node(target)

        if not src_node:
            return {"error": f"Source entity '{source}' not found in causal graph.", "paths": []}
        if not tgt_node:
            return {"error": f"Target entity '{target}' not found in causal graph.", "paths": []}

        paths = graph.find_paths(src_node.id, tgt_node.id, max_depth=max_depth)
        return {
            "source": src_node.label,
            "target": tgt_node.label,
            "path_count": len(paths),
            "paths": paths,
        }

    @classmethod
    def analyze_root_cause(
        cls, graph: CausalKnowledgeGraph, incident_identifier: str, depth: int = 5
    ) -> Dict[str, Any]:
        """Performs root-cause analysis distinguishing:

        - ROOT CAUSE (originating upstream cause with direct evidence)
        - CONTRIBUTING FACTOR (amplifying condition or intermediate vulnerability)
        - SYMPTOM (immediate observable effect)
        """
        logger.info(f"[ROOT_CAUSE_ANALYSIS] Target='{incident_identifier}' Depth={depth}")
        node = graph.find_node(incident_identifier)
        if not node:
            return {
                "error": f"Incident entity '{incident_identifier}' not found in causal graph.",
                "root_cause": None,
                "contributing_factors": [],
                "symptoms": [],
            }

        ancestors = graph.get_ancestors(node.id, max_depth=depth)
        descendants = graph.get_descendants(node.id, max_depth=depth)

        root_causes = []
        contributing_factors = []
        unresolved_hypotheses = []

        for anc in ancestors:
            rel = anc.get("relationship", "").upper()
            conf = anc.get("confidence", 0.0)

            # Check if this node itself has further upstream causes in the graph
            parent_node_id = anc["node_id"]
            has_further_parents = len(graph.incoming.get(parent_node_id, [])) > 0

            # Distinction criteria
            if rel in {"CAUSES", "FAILED_BECAUSE_OF", "RESULTED_IN"} and conf >= 0.80 and not has_further_parents:
                root_causes.append({
                    "entity": anc["label"],
                    "entity_type": anc["entity_type"],
                    "relationship": rel,
                    "confidence": conf,
                    "distance": anc["distance"],
                    "evidence": anc.get("evidence", {}),
                })
            elif rel in {"CONTRIBUTES_TO", "AMPLIFIES", "DEPENDS_ON", "PRECEDED", "CORRELATED_WITH"}:
                contributing_factors.append({
                    "entity": anc["label"],
                    "entity_type": anc["entity_type"],
                    "relationship": rel,
                    "confidence": conf,
                    "distance": anc["distance"],
                    "evidence": anc.get("evidence", {}),
                })
            else:
                if conf < 0.70:
                    unresolved_hypotheses.append({
                        "hypothesis": f"{anc['label']} ({rel}) -> {node.label}",
                        "confidence": conf,
                        "reason": "Insufficient empirical evidence to confirm direct causality.",
                    })
                else:
                    contributing_factors.append({
                        "entity": anc["label"],
                        "entity_type": anc["entity_type"],
                        "relationship": rel,
                        "confidence": conf,
                        "distance": anc["distance"],
                        "evidence": anc.get("evidence", {}),
                    })

        # Symptoms: immediate downstream manifestations
        symptoms = [
            {
                "entity": d["label"],
                "entity_type": d["entity_type"],
                "relationship": d["relationship"],
                "confidence": d["confidence"],
                "evidence": d.get("evidence", {}),
            }
            for d in descendants if d["distance"] == 1
        ]

        # Select primary root cause if available
        primary_root = root_causes[0] if root_causes else (
            contributing_factors[0] if contributing_factors else None
        )

        return {
            "incident": node.label,
            "immediate_cause": primary_root.get("entity") if primary_root else "Unidentified",
            "root_causes": root_causes,
            "contributing_factors": contributing_factors,
            "upstream_causes": ancestors,
            "downstream_effects": descendants,
            "symptoms": symptoms,
            "unresolved_hypotheses": unresolved_hypotheses,
            "confidence": primary_root.get("confidence", 0.5) if primary_root else 0.5,
        }

    @classmethod
    def analyze_cascade(
        cls, graph: CausalKnowledgeGraph, trigger_identifier: str, depth: int = 5
    ) -> Dict[str, Any]:
        """Calculates downstream cascade paths, affected entities, and severity."""
        logger.info(f"[CASCADE_ANALYSIS] Trigger='{trigger_identifier}' Depth={depth}")
        node = graph.find_node(trigger_identifier)
        if not node:
            return {
                "error": f"Trigger entity '{trigger_identifier}' not found in causal graph.",
                "affected_entities": [],
            }

        descendants = graph.get_descendants(node.id, max_depth=depth)

        affected_entities = []
        severity = "low"
        cascade_paths = []

        critical_keywords = ["outage", "escalation", "sla", "revenue", "churn", "loss", "failure"]
        high_severity_count = 0

        for d in descendants:
            label_lower = d["label"].lower()
            entity_severity = "low"
            if any(k in label_lower for k in critical_keywords):
                entity_severity = "high"
                high_severity_count += 1
            elif d["relationship"] in {"CAUSES", "RESULTED_IN", "FAILED_BECAUSE_OF"}:
                entity_severity = "medium"

            affected_entities.append({
                "entity": d["label"],
                "entity_type": d["entity_type"],
                "relationship": d["relationship"],
                "distance": d["distance"],
                "impact_severity": entity_severity,
                "confidence": d["confidence"],
                "evidence": d.get("evidence", {}),
            })

            cascade_paths.append(f"{node.label} --[{d['relationship']}]--> {d['label']} (dist={d['distance']})")

        if high_severity_count >= 2:
            severity = "critical"
        elif high_severity_count == 1 or len(descendants) >= 3:
            severity = "high"
        elif len(descendants) > 0:
            severity = "medium"

        return {
            "trigger": node.label,
            "severity": severity,
            "cascade_paths": cascade_paths,
            "affected_entities": affected_entities,
            "total_downstream_entities": len(affected_entities),
            "evidence": {
                "trigger_type": node.entity_type,
                "total_effects": len(descendants),
            },
        }


causal_inference = CausalInferenceEngine()
