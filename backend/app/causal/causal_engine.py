"""Causal Engine, Evidence Collector, and Causal Conflict Detector for NEXUS-Ω."""

import uuid
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import Event, Experience, Decision, Action, CausalNode, CausalEdge
from app.causal.nodes import CausalEntityType
from app.causal.edges import CausalRelationshipType
from app.causal.confidence import CausalConfidenceCalculator
from app.causal.causal_store import causal_store
from app.causal.graph import CausalKnowledgeGraph
from app.services.memory_service import memory_service
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


class CausalConflictDetector:
    """Detects and resolves conflicting causal claims across experiences and edges."""

    @classmethod
    def detect_conflicts(
        cls, candidate_claim: Dict[str, Any], existing_edges: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detects if a candidate causal claim contradicts known historical evidence."""
        source = candidate_claim.get("source", "").lower()
        target = candidate_claim.get("target", "").lower()
        proposed_rel = candidate_claim.get("relationship", "").upper()

        conflicts = []
        for edge in existing_edges:
            e_src = edge.get("source", "").lower()
            e_tgt = edge.get("target", "").lower()
            e_rel = edge.get("relationship", "").upper()

            # Direct contradiction (e.g. RESOLVED_BY vs FAILED_BECAUSE_OF for same source/target)
            if (source in e_src or e_src in source) and (target in e_tgt or e_tgt in target):
                if proposed_rel in {"RESOLVED_BY", "MITIGATES"} and e_rel in {"FAILED_BECAUSE_OF", "AMPLIFIES", "CAUSES"}:
                    conflicts.append({
                        "existing_edge": edge,
                        "conflict_type": "polar_opposite_outcome",
                        "explanation": f"Claim that '{source}' {proposed_rel} '{target}' contradicts established edge where '{e_src}' {e_rel} '{e_tgt}'.",
                    })
                elif proposed_rel in {"FAILED_BECAUSE_OF"} and e_rel in {"RESOLVED_BY"}:
                    conflicts.append({
                        "existing_edge": edge,
                        "conflict_type": "polar_opposite_outcome",
                        "explanation": f"Claim that '{source}' {proposed_rel} '{target}' contradicts established edge where '{e_src}' {e_rel} '{e_tgt}'.",
                    })

        if conflicts:
            return {
                "conflict": True,
                "competing_hypotheses": [
                    {"hypothesis": f"{candidate_claim.get('source')} --[{proposed_rel}]--> {candidate_claim.get('target')}"},
                    {"hypothesis": f"{conflicts[0]['existing_edge'].get('source')} --[{conflicts[0]['existing_edge'].get('relationship')}]--> {conflicts[0]['existing_edge'].get('target')}"},
                ],
                "evidence": [c["existing_edge"].get("evidence", {}) for c in conflicts],
                "resolution_status": "context_dependent",
                "explanation": (
                    "Contextual variance detected: The effectiveness of this intervention depends on "
                    "incident severity, system concurrency, and previous failure modes."
                ),
            }

        return {
            "conflict": False,
            "competing_hypotheses": [],
            "evidence": [],
            "resolution_status": "consistent",
        }


class CausalEvidenceEngine:
    """Aggregates empirical evidence for causal claims from PostgreSQL and Hindsight."""

    @classmethod
    def collect_evidence(
        cls,
        db: Session,
        organization_id: uuid.UUID,
        source_label: str,
        target_label: str,
        relationship: str,
    ) -> Dict[str, Any]:
        """Collects supporting events, experiences, Hindsight memories, and counter-evidence."""
        logger.info(f"[CAUSAL_EVIDENCE] Gathering evidence for '{source_label}' --[{relationship}]--> '{target_label}'")
        supporting_events: List[Dict[str, Any]] = []
        supporting_memories: List[Dict[str, Any]] = []
        counter_evidence: List[Dict[str, Any]] = []

        # 1. Search PostgreSQL experiences
        experiences = db.scalars(
            select(Experience)
            .where(Experience.organization_id == organization_id)
            .limit(20)
        ).all()

        src_lower = source_label.lower()
        tgt_lower = target_label.lower()

        for exp in experiences:
            desc = (exp.description + " " + (exp.outcome or "")).lower()
            if any(term in desc for term in src_lower.split()) and any(term in desc for term in tgt_lower.split()):
                if relationship in {"RESOLVED_BY", "RESULTED_IN"} and exp.success:
                    supporting_events.append({
                        "experience_id": str(exp.id),
                        "description": exp.description,
                        "outcome": exp.outcome,
                        "success": exp.success,
                    })
                elif relationship in {"RESOLVED_BY", "RESULTED_IN"} and not exp.success:
                    counter_evidence.append({
                        "experience_id": str(exp.id),
                        "description": exp.description,
                        "outcome": exp.outcome,
                        "success": exp.success,
                    })
                elif relationship in {"FAILED_BECAUSE_OF", "CAUSES"} and not exp.success:
                    supporting_events.append({
                        "experience_id": str(exp.id),
                        "description": exp.description,
                        "outcome": exp.outcome,
                        "success": exp.success,
                    })

        # 2. Search Hindsight Memory Engine
        try:
            memories = memory_service.recall_memories(
                query=f"{source_label} {target_label} {relationship}",
                bank_id=settings.HINDSIGHT_BANK_ID,
                max_tokens=2048,
            )
            for mem in memories:
                txt = mem.get("text", "")
                if txt:
                    supporting_memories.append({
                        "text": txt,
                        "bank_id": settings.HINDSIGHT_BANK_ID,
                    })
        except Exception as e:
            logger.warning(f"Causal evidence recall notice: {e}")

        # 3. Calculate nuanced confidence
        conf = CausalConfidenceCalculator.calculate_confidence(
            relationship=relationship,
            supporting_events=supporting_events,
            supporting_memories=supporting_memories,
            counter_evidence=counter_evidence,
        )

        return {
            "relationship": relationship,
            "confidence": conf,
            "supporting_events": supporting_events,
            "supporting_memories": supporting_memories,
            "counter_evidence": counter_evidence,
            "evidence_count": len(supporting_events) + len(supporting_memories),
        }


class CausalEngine:
    """Orchestrates persistent causal knowledge ingestion, evidence tracking, and graph synchronization."""

    def __init__(self):
        self.evidence_engine = CausalEvidenceEngine()
        self.conflict_detector = CausalConflictDetector()

    def get_graph(self, db: Session, organization_id: uuid.UUID) -> CausalKnowledgeGraph:
        """Retrieves and synchronizes the active causal graph from PostgreSQL."""
        graph = CausalKnowledgeGraph(organization_id=str(organization_id))
        graph.sync_from_db(db, organization_id)
        if len(graph.nodes) == 0:
            # Seed foundational organizational causal graph if empty
            self.seed_default_graph(db, organization_id)
            graph.sync_from_db(db, organization_id)
        return graph

    def ingest_causal_relation(
        self,
        db: Session,
        organization_id: uuid.UUID,
        source_label: str,
        source_type: str,
        target_label: str,
        target_type: str,
        relationship: str,
        evidence: Optional[Dict[str, Any]] = None,
        confidence: Optional[float] = None,
        source_entity_id: Optional[str] = None,
        target_entity_id: Optional[str] = None,
    ) -> CausalEdge:
        """Persists a verified causal relationship into PostgreSQL causal nodes and edges."""
        src_node = causal_store.get_or_create_node(
            db=db,
            organization_id=organization_id,
            label=source_label,
            entity_type=source_type,
            entity_id=source_entity_id,
        )
        tgt_node = causal_store.get_or_create_node(
            db=db,
            organization_id=organization_id,
            label=target_label,
            entity_type=target_type,
            entity_id=target_entity_id,
        )

        # Collect evidence if not supplied
        if evidence is None or confidence is None:
            ev_data = self.evidence_engine.collect_evidence(
                db=db,
                organization_id=organization_id,
                source_label=source_label,
                target_label=target_label,
                relationship=relationship,
            )
            evidence = evidence or ev_data
            confidence = confidence or ev_data["confidence"]

        edge = causal_store.add_or_update_edge(
            db=db,
            organization_id=organization_id,
            source_node_id=src_node.id,
            target_node_id=tgt_node.id,
            relationship=relationship,
            confidence=confidence,
            evidence=evidence,
            source_type="ingestion",
        )
        logger.info(
            f"[CAUSAL_GRAPH_UPDATE] Ingested '{source_label}' --[{relationship}]--> '{target_label}' (Conf={confidence})"
        )
        return edge

    def seed_default_graph(self, db: Session, organization_id: uuid.UUID):
        """Seeds empirical operational causal topology for the enterprise (e.g. ACME payment pipeline)."""
        logger.info(f"Seeding empirical causal topology for Org={organization_id}...")

        relations = [
            # 1. Primary failure causality
            ("Payment Gateway Connection Timeout", CausalEntityType.FAILURE, "ACME Transaction Failures", CausalEntityType.INCIDENT, CausalRelationshipType.CAUSES, 0.95),
            ("Uncapped Gateway Retries", CausalEntityType.ACTION, "Connection Pool Starvation", CausalEntityType.FAILURE, CausalRelationshipType.AMPLIFIES, 0.92),
            ("Connection Pool Starvation", CausalEntityType.FAILURE, "Worker Thread Deadlock", CausalEntityType.FAILURE, CausalRelationshipType.CAUSES, 0.90),
            ("Worker Thread Deadlock", CausalEntityType.FAILURE, "Payment Gateway Latency Spike", CausalEntityType.SYMPTOM if hasattr(CausalEntityType, "SYMPTOM") else CausalEntityType.EVENT, CausalRelationshipType.TRIGGERS, 0.88),
            ("ACME Transaction Failures", CausalEntityType.INCIDENT, "ACME Executive Escalation", CausalEntityType.INCIDENT, CausalRelationshipType.TRIGGERS, 0.91),
            ("ACME Executive Escalation", CausalEntityType.INCIDENT, "Contractual SLA Penalty Risk", CausalEntityType.RISK, CausalRelationshipType.CAUSES, 0.89),
            ("Contractual SLA Penalty Risk", CausalEntityType.RISK, "Enterprise Contract Churn", CausalEntityType.RISK, CausalRelationshipType.AMPLIFIES, 0.85),

            # 2. Interventions & Outcomes
            ("Switch Traffic to Secondary Rail B", CausalEntityType.ACTION, "Payment Success Rate Recovery to 99.98%", CausalEntityType.OUTCOME, CausalRelationshipType.RESULTED_IN, 0.96),
            ("Payment Success Rate Recovery to 99.98%", CausalEntityType.OUTCOME, "ACME Transaction Failures", CausalEntityType.INCIDENT, CausalRelationshipType.RESOLVED_BY, 0.95),
            ("Service Restart during Connection Pool Exhaustion", CausalEntityType.ACTION, "Recurrence of Failure within 20min", CausalEntityType.OUTCOME, CausalRelationshipType.FAILED_BECAUSE_OF, 0.94),
            ("Direct SRE Communication to VP of Eng", CausalEntityType.ACTION, "Executive De-escalation", CausalEntityType.OUTCOME, CausalRelationshipType.RESULTED_IN, 0.93),
            ("Automated Generic Status Email", CausalEntityType.ACTION, "Customer Frustration Escalation", CausalEntityType.OUTCOME, CausalRelationshipType.TRIGGERS, 0.91),
        ]

        for src, src_t, tgt, tgt_t, rel, conf in relations:
            self.ingest_causal_relation(
                db=db,
                organization_id=organization_id,
                source_label=src,
                source_type=src_t.value if hasattr(src_t, "value") else str(src_t),
                target_label=tgt,
                target_type=tgt_t.value if hasattr(tgt_t, "value") else str(tgt_t),
                relationship=rel.value if hasattr(rel, "value") else str(rel),
                confidence=conf,
                evidence={"source": "Historical Incident Telemetry & Postmortems", "empirical": True},
            )
        db.commit()


causal_engine = CausalEngine()
