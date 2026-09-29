"""Organization Model."""

import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, func, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.customer import Customer
    from app.db.models.event import Event
    from app.db.models.experience import Experience
    from app.db.models.decision import Decision
    from app.db.models.action import Action
    from app.db.models.agent_run import AgentRun
    from app.db.models.memory_reference import MemoryReference


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    users: Mapped[List["User"]] = relationship(
        "User", back_populates="organization", cascade="all, delete-orphan"
    )
    customers: Mapped[List["Customer"]] = relationship(
        "Customer", back_populates="organization", cascade="all, delete-orphan"
    )
    events: Mapped[List["Event"]] = relationship(
        "Event", back_populates="organization", cascade="all, delete-orphan"
    )
    experiences: Mapped[List["Experience"]] = relationship(
        "Experience", back_populates="organization", cascade="all, delete-orphan"
    )
    decisions: Mapped[List["Decision"]] = relationship(
        "Decision", back_populates="organization", cascade="all, delete-orphan"
    )
    actions: Mapped[List["Action"]] = relationship(
        "Action", back_populates="organization", cascade="all, delete-orphan"
    )
    agent_runs: Mapped[List["AgentRun"]] = relationship(
        "AgentRun", back_populates="organization", cascade="all, delete-orphan"
    )
    memory_references: Mapped[List["MemoryReference"]] = relationship(
        "MemoryReference", back_populates="organization", cascade="all, delete-orphan"
    )
