"""Causal Knowledge Graph & Inference API Router."""

import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.causal.causal_engine import causal_engine
from app.causal.inference import causal_inference
from app.schemas.causal_api import (
    RootCauseRequest,
    RootCauseResponse,
    CausalPathResponse,
    CascadeRequest,
    CascadeResponse,
)
from app.core.logging import logger

router = APIRouter(prefix="/causal", tags=["Causal Intelligence"])


@router.post("/root-cause", response_model=RootCauseResponse, summary="Perform Root Cause Analysis")
def analyze_root_cause(payload: RootCauseRequest, db: Session = Depends(get_db)):
    """Traces upstream causality to identify true root causes, contributing factors, and symptoms."""
    try:
        graph = causal_engine.get_graph(db, payload.organization_id)
        result = causal_inference.analyze_root_cause(
            graph=graph,
            incident_identifier=payload.incident_id,
            depth=payload.depth,
        )
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return RootCauseResponse(
            incident=result["incident"],
            immediate_cause=result.get("immediate_cause"),
            root_causes=result.get("root_causes", []),
            contributing_factors=result.get("contributing_factors", []),
            upstream_causes=result.get("upstream_causes", []),
            downstream_effects=result.get("downstream_effects", []),
            symptoms=result.get("symptoms", []),
            unresolved_hypotheses=result.get("unresolved_hypotheses", []),
            confidence=result.get("confidence", 0.5),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing root cause: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/path", response_model=CausalPathResponse, summary="Find Strongest Causal Paths")
def get_causal_path(
    source: str = Query(..., description="Source entity name or ID"),
    target: str = Query(..., description="Target entity name or ID"),
    organization_id: uuid.UUID = Query(..., description="Organization ID"),
    depth: int = Query(5, ge=1, le=10, description="Max traversal depth"),
    db: Session = Depends(get_db),
):
    """Finds directed causal chains connecting source to target with confidence and evidence."""
    try:
        graph = causal_engine.get_graph(db, organization_id)
        result = causal_inference.find_paths(
            graph=graph,
            source=source,
            target=target,
            max_depth=depth,
        )
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return CausalPathResponse(
            source=result["source"],
            target=result["target"],
            path_count=result["path_count"],
            paths=result.get("paths", []),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error finding causal path: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cascade", response_model=CascadeResponse, summary="Predict Downstream Cascading Impacts")
def analyze_cascade(payload: CascadeRequest, db: Session = Depends(get_db)):
    """Predicts downstream ripple effects, affected entities, and severity from a trigger event or action."""
    try:
        graph = causal_engine.get_graph(db, payload.organization_id)
        result = causal_inference.analyze_cascade(
            graph=graph,
            trigger_identifier=payload.trigger,
            depth=payload.depth,
        )
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return CascadeResponse(
            trigger=result["trigger"],
            severity=result["severity"],
            cascade_paths=result.get("cascade_paths", []),
            affected_entities=result.get("affected_entities", []),
            total_downstream_entities=result.get("total_downstream_entities", 0),
            evidence=result.get("evidence", {}),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing cascade: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/graph", summary="Get Full Causal Knowledge Graph")
def get_causal_graph(organization_id: Optional[uuid.UUID] = None, db: Session = Depends(get_db)):
    """Retrieves full persistent causal topology for visualization in React Flow."""
    target_org = organization_id or uuid.UUID("2d48f08c-0b35-4aea-8941-86e4f855f738")
    graph = causal_engine.get_graph(db, target_org)
    return graph.to_dict()
