"""AgentReflection Model - Stores outcome comparisons and extracted lessons learned."""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any, TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, ForeignKey, JSON, func, Uuid, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.organization import Organization


class AgentReflection(Base):
    __tablename__ = "agent_reflections"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    request_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    agent_name: Mapped[str] = mapped_column(String(100), default="ReflectionAgent", nullable=False)
    decision_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("decisions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    expected_outcome: Mapped[str] = mapped_column(Text, nullable=False)
    actual_outcome: Mapped[str] = mapped_column(Text, nullable=False)
    what_worked: Mapped[str] = mapped_column(Text, nullable=False)
    what_failed: Mapped[str] = mapped_column(Text, nullable=False)
    lessons_learned: Mapped[str] = mapped_column(Text, nullable=False)
    hindsight_bank_id: Mapped[str] = mapped_column(String(255), nullable=False)
    hindsight_document_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    organization: Mapped["Organization"] = relationship("Organization", backref="agent_reflections")

    __table_args__ = (
        Index("ix_agent_reflections_req", "organization_id", "request_id"),
    )
