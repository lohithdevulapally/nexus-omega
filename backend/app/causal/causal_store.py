"""Persistent Causal Store bridging SQLAlchemy models with graph representations."""

import uuid
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.db.models.causal import CausalNode, CausalEdge
from app.causal.nodes import CausalNodeDTO
from app.causal.edges import CausalEdgeDTO
from app.core.logging import logger


class CausalStore:
    """Manages persistence of causal nodes and edges in PostgreSQL."""

    @staticmethod
    def get_or_create_node(
        db: Session,
        organization_id: uuid.UUID,
        label: str,
        entity_type: str,
        entity_id: Optional[str] = None,
        description: Optional[str] = None,
        metadata_json: Optional[Dict[str, Any]] = None,
    ) -> CausalNode:
        """Finds existing node by label or entity_id, or creates a new one."""
        query = select(CausalNode).where(
            CausalNode.organization_id == organization_id,
            CausalNode.label == label
        )
        if entity_id:
            query = select(CausalNode).where(
                CausalNode.organization_id == organization_id,
                and_(CausalNode.entity_type == entity_type, CausalNode.entity_id == entity_id)
            )

        existing = db.scalars(query).first()
        if existing:
            return existing

        node = CausalNode(
            id=uuid.uuid4(),
            organization_id=organization_id,
            entity_type=entity_type,
            entity_id=entity_id,
            label=label,
            description=description,
            metadata_json=metadata_json or {},
        )
        db.add(node)
        db.flush()
        return node

    @staticmethod
    def add_or_update_edge(
        db: Session,
        organization_id: uuid.UUID,
        source_node_id: uuid.UUID,
        target_node_id: uuid.UUID,
        relationship: str,
        confidence: float,
        evidence: Dict[str, Any],
        source_type: str = "inference",
    ) -> CausalEdge:
        """Finds or creates a directed causal edge between two nodes."""
        existing = db.scalars(
            select(CausalEdge).where(
                CausalEdge.organization_id == organization_id,
                CausalEdge.source_node_id == source_node_id,
                CausalEdge.target_node_id == target_node_id,
                CausalEdge.relationship == relationship,
            )
        ).first()

        if existing:
            # Update confidence and append evidence
            existing.confidence = max(existing.confidence, confidence)
            merged_evidence = dict(existing.evidence)
            merged_evidence.update(evidence)
            existing.evidence = merged_evidence
            db.flush()
            return existing

        edge = CausalEdge(
            id=uuid.uuid4(),
            organization_id=organization_id,
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            relationship=relationship,
            confidence=confidence,
            evidence=evidence,
            source_type=source_type,
        )
        db.add(edge)
        db.flush()
        return edge

    @staticmethod
    def load_graph_data(
        db: Session, organization_id: uuid.UUID
    ) -> Tuple[List[CausalNodeDTO], List[CausalEdgeDTO]]:
        """Loads all nodes and edges for an organization from PostgreSQL."""
        nodes = db.scalars(
            select(CausalNode).where(CausalNode.organization_id == organization_id)
        ).all()

        edges = db.scalars(
            select(CausalEdge).where(CausalEdge.organization_id == organization_id)
        ).all()

        node_dtos = [
            CausalNodeDTO(
                id=str(n.id),
                organization_id=str(n.organization_id),
                entity_type=n.entity_type,
                entity_id=n.entity_id,
                label=n.label,
                description=n.description,
                metadata_json=n.metadata_json,
                created_at=n.created_at.isoformat() if n.created_at else None,
                updated_at=n.updated_at.isoformat() if n.updated_at else None,
            )
            for n in nodes
        ]

        edge_dtos = [
            CausalEdgeDTO(
                id=str(e.id),
                organization_id=str(e.organization_id),
                source_node_id=str(e.source_node_id),
                target_node_id=str(e.target_node_id),
                relationship=e.relationship,
                confidence=e.confidence,
                evidence=e.evidence,
                source_type=e.source_type,
                created_at=e.created_at.isoformat() if e.created_at else None,
            )
            for e in edges
        ]

        return node_dtos, edge_dtos


causal_store = CausalStore()
