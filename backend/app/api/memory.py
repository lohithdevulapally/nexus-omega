"""Hindsight Memory API Router."""

import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.memory import (
    MemoryRetainRequest,
    MemoryRetainResponse,
    MemorySearchResponse,
    MemoryReflectRequest,
    MemoryReflectResponse,
)
from app.services.memory_service import memory_service
from app.services.event_service import event_service
from app.core.config import get_settings

router = APIRouter(prefix="/memory", tags=["Hindsight Memory"])
settings = get_settings()


@router.post("/retain", response_model=MemoryRetainResponse, summary="Retain Experience")
def retain_memory(payload: MemoryRetainRequest, db: Session = Depends(get_db)):
    """Retains an operational experience narrative in Hindsight and PostgreSQL."""
    try:
        exp = event_service.create_experience(
            db=db,
            organization_id=payload.organization_id,
            experience_type=payload.experience_type,
            description=payload.content,
            outcome="Retained via /memory/retain API",
            action_taken=payload.experience_type,
            success=True,
            metadata=payload.metadata,
            retain_in_hindsight=True,
        )
        return MemoryRetainResponse(
            success=True,
            bank_id=settings.HINDSIGHT_BANK_ID,
            experience_id=exp.id,
            message="Experience retained in Hindsight and synchronized to PostgreSQL.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retain memory: {str(e)}")


@router.get("/search", response_model=MemorySearchResponse, summary="Search Hindsight Memory")
def search_memory(
    query: str = Query(..., description="Semantic search query"),
    organization_id: uuid.UUID = Query(..., description="Organization ID"),
    limit: int = Query(10, ge=1, le=50),
):
    """Searches the Hindsight memory bank for experiences matching the query."""
    try:
        memories = memory_service.recall_memories(
            query=query,
            bank_id=settings.HINDSIGHT_BANK_ID,
            max_tokens=4096,
        )
        return MemorySearchResponse(
            bank_id=settings.HINDSIGHT_BANK_ID,
            query=query,
            count=len(memories),
            memories=memories[:limit],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Memory search failed: {str(e)}")


@router.post("/reflect", response_model=MemoryReflectResponse, summary="Reflect on Hindsight Memory")
def reflect_memory(payload: MemoryReflectRequest):
    """Generates an organizational reflection and learned synthesis over Hindsight memories."""
    try:
        result = memory_service.reflect_on_memories(
            query=payload.query,
            bank_id=settings.HINDSIGHT_BANK_ID,
            context=payload.context,
        )
        return MemoryReflectResponse(
            bank_id=settings.HINDSIGHT_BANK_ID,
            query=payload.query,
            reflection=result.get("text", ""),
            based_on=result.get("based_on") or [],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Memory reflection failed: {str(e)}")


@router.get("/experiences", summary="List All Retained Experiences")
def list_experiences(
    organization_id: Optional[uuid.UUID] = None,
    experience_type: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Retrieves list of retained operational experiences with outcomes and lessons."""
    from app.db.models import Experience
    query = db.query(Experience)
    if organization_id:
        query = query.filter(Experience.organization_id == organization_id)
    if experience_type:
        query = query.filter(Experience.experience_type == experience_type)
    exps = query.order_by(Experience.created_at.desc()).limit(limit).all()
    return [
        {
            "id": str(e.id),
            "organization_id": str(e.organization_id),
            "experience_type": e.experience_type,
            "description": e.description,
            "action_taken": e.action_taken,
            "outcome": e.outcome,
            "success": e.success,
            "hindsight_bank_id": e.hindsight_bank_id,
            "hindsight_document_id": e.hindsight_document_id,
            "metadata": e.metadata_json or {},
            "created_at": e.created_at.isoformat() if e.created_at else None,
        }
        for e in exps
    ]
