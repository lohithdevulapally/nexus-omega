"""Multi-Agent API Router."""

import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.agent_api import AgentInvestigateRequest, AgentInvestigateResponse
from app.agents.orchestrator import orchestrator
from app.core.logging import logger

router = APIRouter(prefix="/agents", tags=["Multi-Agent Intelligence"])


@router.post("/investigate", response_model=AgentInvestigateResponse, summary="Autonomous Multi-Agent Investigation")
def investigate_agent_flow(payload: AgentInvestigateRequest, db: Session = Depends(get_db)):
    """Executes the complete multi-agent graph across Planner, Memory, Analyst, Causal, Risk, Decision, Critic, and Reflection agents."""
    try:
        state = orchestrator.run_investigation(
            db=db,
            organization_id=payload.organization_id,
            user_request=payload.request,
            user_id=payload.user_id,
        )

        return AgentInvestigateResponse(
            request_id=state.request_id,
            status=state.status,
            plan=state.planner_output,
            memories=state.recalled_memories,
            findings=state.analyst_output.get("findings", []),
            causal_analysis=state.causal_output,
            risks=state.risk_output,
            decision_candidates=state.decision_output.get("candidates", []),
            critique=state.critic_output,
            final_recommendation=state.final_recommendation or "No recommendation generated.",
            approval_required=state.approval_required,
            provenance=state.provenance,
            simulation=state.simulation_output,
            action_id=state.action_id,
            action_request=state.action_request,
            timeline=state.timeline,
        )
    except Exception as e:
        logger.error(f"Error in multi-agent investigation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Agent investigation failed: {str(e)}")


@router.get("/runs", summary="List Agent Execution Runs")
def list_agent_runs(
    organization_id: Optional[uuid.UUID] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Lists historical agent execution runs from the agent_runs log."""
    from app.db.models import AgentRun
    query = db.query(AgentRun)
    if organization_id:
        query = query.filter(AgentRun.organization_id == organization_id)
    runs = query.order_by(AgentRun.started_at.desc()).limit(limit).all()
    return [
        {
            "id": str(r.id),
            "agent_name": r.agent_name,
            "task": r.task,
            "status": r.status,
            "duration_ms": (r.output_data or {}).get("duration_ms", 0) if isinstance(r.output_data, dict) else 0,
            "input_data": r.input_data,
            "output_data": r.output_data,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
        }
        for r in runs
    ]
