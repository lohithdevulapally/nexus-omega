"""Events API Router."""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import get_db
from app.db.models import Event
from app.schemas.event import EventCreate, EventResponse
from app.services.event_service import event_service

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("", response_model=EventResponse, summary="Ingest Event")
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    """Ingests a new enterprise event into PostgreSQL."""
    event = event_service.create_event(
        db=db,
        organization_id=payload.organization_id,
        event_type=payload.event_type,
        title=payload.title,
        description=payload.description,
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
        source=payload.source,
        metadata=payload.metadata_json,
    )
    return event


@router.get("", response_model=List[EventResponse], summary="List Events")
def list_events(
    organization_id: uuid.UUID = Query(..., description="Organization ID"),
    entity_id: Optional[str] = Query(None, description="Filter by Entity ID"),
    event_type: Optional[str] = Query(None, description="Filter by Event Type"),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Lists events filtered by entity or type."""
    stmt = select(Event).where(Event.organization_id == organization_id)
    if entity_id:
        stmt = stmt.where(Event.entity_id == entity_id)
    if event_type:
        stmt = stmt.where(Event.event_type == event_type)
    stmt = stmt.order_by(Event.created_at.desc()).limit(limit)
    return list(db.scalars(stmt).all())
