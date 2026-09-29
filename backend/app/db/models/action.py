"""Action Model."""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON, func, Uuid, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.organization import Organization
    from app.db.models.decision import Decision


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    decision_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("decisions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    agent_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    approval_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    approval_status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    requested_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    risk_level: Mapped[str] = mapped_column(String(50), default="low", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    execution_status: Mapped[str] = mapped_column(String(50), default="not_started", nullable=False)
    result: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    organization: Mapped["Organization"] = relationship("Organization", back_populates="actions")
    decision: Mapped[Optional["Decision"]] = relationship("Decision", back_populates="actions")

    __table_args__ = (
        Index("ix_actions_org_status", "organization_id", "status"),
    )
