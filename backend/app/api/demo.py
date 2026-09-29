"""Demo Management API Router for NEXUS-Ω."""

import uuid
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import delete

from app.db.database import get_db
from app.db.models import Action, AgentDecision, AgentRun, AgentObservation, AgentReflection, Event
from app.services.audit_service import audit_service
from app.core.security import require_permission, Permission, AuthContext, DEFAULT_DEMO_ORG_ID

router = APIRouter(prefix="/demo", tags=["Demo Management"])


@router.post("/reset", summary="Reset Demo State for Live Presentations")
def reset_demo_state(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission(Permission.INVESTIGATE)),
):
    """Safely resets demo organization state (clearing pending test actions and transient runs)

    Allows unlimited repeated live hackathon demonstrations without affecting real production data.
    """
    demo_org_id = DEFAULT_DEMO_ORG_ID

    # Reset all transient actions created during demo runs for the demo organization
    actions_deleted = db.query(Action).filter(
        Action.organization_id == demo_org_id,
    ).delete(synchronize_session=False)

    # Clean up recent agent runs and observations
    runs_deleted = db.query(AgentRun).filter(AgentRun.organization_id == demo_org_id).delete(synchronize_session=False)
    decisions_deleted = db.query(AgentDecision).filter(AgentDecision.organization_id == demo_org_id).delete(synchronize_session=False)
    obs_deleted = db.query(AgentObservation).filter(AgentObservation.organization_id == demo_org_id).delete(synchronize_session=False)
    ref_deleted = db.query(AgentReflection).filter(AgentReflection.organization_id == demo_org_id).delete(synchronize_session=False)

    db.commit()

    # Re-verify and ensure foundational demo seed entities exist
    from app.db.database import ensure_seed_data
    ensure_seed_data(db)

    audit_service.log_event(
        db=db,
        organization_id=demo_org_id,
        event_type="DEMO_RESET",
        user_id=auth.user_id,
        result="success",
        details={
            "actions_cleared": actions_deleted,
            "agent_runs_cleared": runs_deleted,
        },
    )

    return {
        "status": "reset_successful",
        "organization_id": str(demo_org_id),
        "actions_cleared": actions_deleted,
        "runs_cleared": runs_deleted,
        "decisions_cleared": decisions_deleted,
        "observations_cleared": obs_deleted,
        "reflections_cleared": ref_deleted,
        "message": "NEXUS-Ω demo environment successfully refreshed for live judging walkthrough.",
    }
