"""Causal Knowledge Graph Models for NEXUS-Ω.

Provides persistent nodes and edges in PostgreSQL representing organizational causal relationships.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List, TYPE_CHECKING
from sqlalchemy import String, Float, DateTime, ForeignKey, JSON, Text, func, Uuid, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship as orm_relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.organization import Organization


class CausalNode(Base):
    __tablename__ = "causal_nodes"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    label: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    organization: Mapped["Organization"] = orm_relationship("Organization")
    outgoing_edges: Mapped[List["CausalEdge"]] = orm_relationship(
        "CausalEdge",
        foreign_keys="[CausalEdge.source_node_id]",
        back_populates="source_node",
        cascade="all, delete-orphan",
    )
    incoming_edges: Mapped[List["CausalEdge"]] = orm_relationship(
        "CausalEdge",
        foreign_keys="[CausalEdge.target_node_id]",
        back_populates="target_node",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_causal_nodes_org_label", "organization_id", "label"),
        Index("ix_causal_nodes_org_entity", "organization_id", "entity_type", "entity_id"),
    )


class CausalEdge(Base):
    __tablename__ = "causal_edges"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_node_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("causal_nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_node_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("causal_nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    relationship: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    evidence: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    source_type: Mapped[str] = mapped_column(String(100), default="inference", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    organization: Mapped["Organization"] = orm_relationship("Organization")
    source_node: Mapped["CausalNode"] = orm_relationship(
        "CausalNode", foreign_keys=[source_node_id], back_populates="outgoing_edges"
    )
    target_node: Mapped["CausalNode"] = orm_relationship(
        "CausalNode", foreign_keys=[target_node_id], back_populates="incoming_edges"
    )

    __table_args__ = (
        Index("ix_causal_edges_org_rel", "organization_id", "relationship"),
        Index("ix_causal_edges_source_target", "source_node_id", "target_node_id", "relationship"),
    )
