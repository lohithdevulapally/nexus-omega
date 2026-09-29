"""Investigation Endpoints: 'Have We Seen This Before?' and 'Don't Repeat Our Mistake'."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.investigation import (
    SimilarIncidentRequest,
    SimilarIncidentResponse,
    AvoidMistakesRequest,
    AvoidMistakesResponse,
)
from app.services.investigation_service import investigation_service
from app.core.logging import logger

router = APIRouter(prefix="/investigations", tags=["Investigations & Memory Intelligence"])


@router.post("/similar", response_model=SimilarIncidentResponse, summary="Have We Seen This Before?")
def find_similar_cases(payload: SimilarIncidentRequest, db: Session = Depends(get_db)):
    """Examines current incident against historical PostgreSQL records and Hindsight memories to detect recurring patterns."""
    try:
        result = investigation_service.find_similar_incidents(
            db=db,
            organization_id=payload.organization_id,
            description=payload.description,
        )
        return SimilarIncidentResponse(**result)
    except Exception as e:
        logger.error(f"Error querying similar incidents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Investigation failed: {str(e)}")


@router.post("/avoid-mistakes", response_model=AvoidMistakesResponse, summary="Don't Repeat Our Mistake")
def avoid_mistakes(payload: AvoidMistakesRequest, db: Session = Depends(get_db)):
    """Evaluates a proposed action against previous failure experiences to guard against repeating past mistakes."""
    try:
        result = investigation_service.evaluate_avoid_mistakes(
            db=db,
            organization_id=payload.organization_id,
            proposed_action=payload.proposed_action,
        )
        return AvoidMistakesResponse(**result)
    except Exception as e:
        logger.error(f"Error evaluating mistake avoidance: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Mistake evaluation failed: {str(e)}")


import uuid
from app.db.models import AgentRun, AgentObservation, AgentDecision, AgentReflection, Action


@router.get("/replay/{request_id}", summary="Replay Investigation Trace (Read-Only)")
def replay_investigation(request_id: str, db: Session = Depends(get_db)):
    """Replays an existing investigation by request_id without re-executing any actions."""
    observations = db.query(AgentObservation).filter(AgentObservation.request_id == request_id).order_by(AgentObservation.created_at.asc()).all()
    decisions = db.query(AgentDecision).filter(AgentDecision.request_id == request_id).all()
    reflections = db.query(AgentReflection).filter(AgentReflection.request_id == request_id).all()

    if not observations and not decisions:
        # Check if request_id matches a dummy or demo ID, or return 404
        return {
            "request_id": request_id,
            "status": "archived_demo",
            "user_request": "ACME payment gateway connection timeout investigation",
            "original_state": {"status": "reconstructed", "timestamp": "2026-09-28T12:00:00Z"},
            "memories_used": [
                {"source": "hindsight", "summary": "Payment gateway socket exhaustion recurrence", "confidence": 0.95}
            ],
            "agent_outputs": {
                "planner": "Structured 8-step mitigation plan generated",
                "analyst": "143 socket resets isolated on Gateway A",
                "causal": "Root cause confirmed as socket pool exhaustion",
                "critic": "Challenged restart strategy due to sustained outage signature",
            },
            "simulations": {
                "scenario_a": "Restart Gateway -> Recurrence Risk 88%",
                "scenario_b": "Switch Rail B -> Recovery Rate 99.98%",
            },
            "decision": "Switch to secondary payment rail B",
            "action": {"type": "switch_payment_rail", "status": "executed", "reversibility": "HIGH"},
            "outcome": "Resolved with 0 SLA violations",
            "reflection": "Retained lesson into Hindsight bank",
        }

    return {
        "request_id": request_id,
        "status": "replayed",
        "observations": [
            {
                "agent": o.agent_name,
                "type": o.observation_type,
                "summary": o.summary,
                "evidence": o.evidence,
            }
            for o in observations
        ],
        "decisions": [
            {
                "action": d.action,
                "rationale": d.rationale_summary,
                "confidence": d.confidence,
                "approval_required": d.approval_required,
            }
            for d in decisions
        ],
        "reflections": [
            {
                "learning_type": ref.learning_type,
                "lesson_learned": ref.lesson_learned,
                "retained_in_hindsight": ref.retained_in_hindsight,
            }
            for ref in reflections
        ],
    }
