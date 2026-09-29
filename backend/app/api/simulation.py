"""Counterfactual Simulation API Router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.simulation.simulator import counterfactual_engine
from app.schemas.simulation_api import (
    CounterfactualRequest,
    CounterfactualResponse,
    CompareScenariosRequest,
    CompareScenariosResponse,
    ReconstructStateRequest,
    ReconstructStateResponse,
)
from app.core.logging import logger

router = APIRouter(prefix="/simulation", tags=["Counterfactual Simulation"])


@router.post("/counterfactual", response_model=CounterfactualResponse, summary="Execute What-If Counterfactual Simulation")
def run_counterfactual(payload: CounterfactualRequest, db: Session = Depends(get_db)):
    """Simulates 'What if we had chosen X instead of Y?', contrasting Actual vs Counterfactual worlds."""
    try:
        result = counterfactual_engine.run_counterfactual(
            db=db,
            organization_id=payload.organization_id,
            incident_id=payload.incident_id,
            alternative_action=payload.alternative_action,
            baseline_action=payload.baseline_action or "switch_to_secondary_rail_b",
        )
        return CounterfactualResponse(
            actual_world=result["actual_world"],
            counterfactual_world=result["counterfactual_world"],
            differences=result["differences"],
            causal_paths=result["causal_paths"],
            historical_evidence=result["historical_evidence"],
            assumptions=result["assumptions"],
            uncertainty=result["uncertainty"],
            confidence=result["confidence"],
        )
    except Exception as e:
        logger.error(f"Error running counterfactual simulation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare", response_model=CompareScenariosResponse, summary="Compare Multiple Candidate Actions")
def compare_scenarios(payload: CompareScenariosRequest, db: Session = Depends(get_db)):
    """Evaluates multiple decision options independently without silently picking a winner."""
    try:
        comparison = counterfactual_engine.compare_scenarios(
            db=db,
            organization_id=payload.organization_id,
            decision_context=payload.decision_context,
            options=payload.options,
        )
        return CompareScenariosResponse(
            comparison_id=comparison.comparison_id,
            decision_context=comparison.decision_context,
            timestamp=comparison.timestamp,
            options_evaluated=comparison.options_evaluated,
            evaluations=comparison.evaluations or comparison.options_evaluated,
            comparative_synthesis=comparison.comparative_synthesis,
        )
    except Exception as e:
        logger.error(f"Error comparing scenarios: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reconstruct", response_model=ReconstructStateResponse, summary="Time-Travel Organizational State Reconstruction")
def reconstruct_historical_state(payload: ReconstructStateRequest, db: Session = Depends(get_db)):
    """Reconstructs organizational knowledge and operational state as it existed at a past timestamp."""
    try:
        snapshot_dict = counterfactual_engine.reconstruct_historical_state(
            db=db,
            organization_id=payload.organization_id,
            timestamp_iso=payload.timestamp,
        )
        return ReconstructStateResponse(
            snapshot_id=snapshot_dict["snapshot_id"],
            organization_id=snapshot_dict["organization_id"],
            timestamp=snapshot_dict["timestamp"],
            source_request=snapshot_dict["source_request"],
            simulation_tag=snapshot_dict["simulation_tag"],
            state_hash=snapshot_dict["state_hash"],
            entities=snapshot_dict["entities"],
            events=snapshot_dict["events"],
            experiences=snapshot_dict["experiences"],
            active_risks=snapshot_dict["active_risks"],
            relevant_memories=snapshot_dict["relevant_memories"],
        )
    except Exception as e:
        logger.error(f"Error reconstructing historical state: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
