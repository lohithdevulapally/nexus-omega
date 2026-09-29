"""Chat API Router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_service
from app.core.logging import logger

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse, summary="Memory-Aware Chat")
def chat_endpoint(payload: ChatRequest, db: Session = Depends(get_db)):
    """Conversational endpoint fusing PostgreSQL state and Hindsight memories.

    Retains meaningful operational experiences into Hindsight and PostgreSQL.
    """
    try:
        response = chat_service.process_chat(
            db=db,
            organization_id=payload.organization_id,
            message=payload.message,
            conversation_id=payload.conversation_id,
        )
        return ChatResponse(**response)
    except Exception as e:
        logger.error(f"Error handling chat message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
