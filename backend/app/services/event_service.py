"""Event and Experience Service."""

import uuid
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models import Event, Experience, MemoryReference
from app.services.memory_service import memory_service
from app.core.logging import logger
from app.core.config import get_settings

settings = get_settings()


class EventService:
    def create_event(
        self,
        db: Session,
        organization_id: uuid.UUID,
        event_type: str,
        title: str,
        description: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        source: str = "system",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Event:
        """Creates an Event record in PostgreSQL."""
        event = Event(
            organization_id=organization_id,
            event_type=event_type,
            title=title,
            description=description,
            entity_type=entity_type,
            entity_id=entity_id,
            source=source,
            metadata_json=metadata or {},
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        logger.info(f"Recorded event '{event.title}' ({event.event_type}) with ID {event.id}")
        return event

    def create_experience(
        self,
        db: Session,
        organization_id: uuid.UUID,
        experience_type: str,
        description: str,
        outcome: str,
        action_taken: Optional[str] = None,
        success: bool = True,
        event_id: Optional[uuid.UUID] = None,
        metadata: Optional[Dict[str, Any]] = None,
        retain_in_hindsight: bool = True,
    ) -> Experience:
        """Creates an Experience in PostgreSQL and retains it in Hindsight with a MemoryReference."""
        bank_id = settings.HINDSIGHT_BANK_ID

        experience = Experience(
            organization_id=organization_id,
            event_id=event_id,
            experience_type=experience_type,
            description=description,
            action_taken=action_taken,
            outcome=outcome,
            success=success,
            hindsight_bank_id=bank_id,
            metadata_json=metadata or {},
        )
        db.add(experience)
        db.commit()
        db.refresh(experience)

        if retain_in_hindsight:
            hindsight_content = (
                f"[{experience_type.upper()}] {description}\n"
                f"Action taken: {action_taken or 'N/A'}\n"
                f"Outcome: {outcome}\n"
                f"Success status: {'SUCCESS' if success else 'FAILURE'}"
            )
            try:
                retain_res = memory_service.retain_experience(
                    content=hindsight_content,
                    bank_id=bank_id,
                    metadata={"experience_id": str(experience.id), "org_id": str(organization_id)},
                    tags=[experience_type, "experience"],
                )
                logger.info(f"Retained experience {experience.id} in Hindsight bank {bank_id}")

                # Store Memory Reference in PostgreSQL
                mem_ref = MemoryReference(
                    organization_id=organization_id,
                    entity_type="experience",
                    entity_id=str(experience.id),
                    hindsight_bank_id=bank_id,
                    memory_context=description[:500],
                    metadata_json=retain_res or {},
                )
                db.add(mem_ref)
                db.commit()
            except Exception as e:
                logger.warning(f"Could not retain experience in Hindsight: {e}")

        return experience

    def get_events_for_entity(
        self, db: Session, organization_id: uuid.UUID, entity_id: str, limit: int = 10
    ) -> List[Event]:
        """Queries recent events for an entity."""
        stmt = (
            select(Event)
            .where(Event.organization_id == organization_id, Event.entity_id == entity_id)
            .order_by(Event.created_at.desc())
            .limit(limit)
        )
        return list(db.scalars(stmt).all())


event_service = EventService()
