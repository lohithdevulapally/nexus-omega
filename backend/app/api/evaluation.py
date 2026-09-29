"""Evaluation API Router for NEXUS-Ω.

Exposes endpoints for Memory A/B Testing, Benchmarks, Causal Precision Metrics,
Performance Latencies, and Chaos Stress-Testing.
"""

import uuid
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import get_db
from app.evaluation.memory_ablation import memory_ablation_engine
from app.evaluation.evaluator import system_evaluator
from app.evaluation.benchmark import performance_benchmarker
from app.evaluation.metrics import MemoryQualityMetrics
from app.chaos.injector import chaos_injector
from app.chaos.runner import chaos_runner
from app.core.security import require_permission, Permission, AuthContext, DEFAULT_DEMO_ORG_ID

router = APIRouter(prefix="/evaluation", tags=["Evaluation & Hardening"])


class MemoryAblationRequest(BaseModel):
    scenario_id: str
    organization_id: Optional[str] = None


class ChaosInjectionRequest(BaseModel):
    scenario_id: str
    organization_id: Optional[str] = None


@router.post("/memory-ablation", summary="Run Memory A/B Ablation Test")
def run_memory_ablation(
    payload: MemoryAblationRequest,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission(Permission.VIEW)),
):
    """Runs identical scenario through Mode A (Without Memory) vs Mode B (With Hindsight)

    Directly demonstrates the tangible advantage of experiential memory.
    """
    org_id = uuid.UUID(payload.organization_id) if payload.organization_id else auth.organization_id
    result = memory_ablation_engine.run_ablation(
        scenario_id=payload.scenario_id,
        organization_id=org_id,
        db=db,
    )
    return result


@router.post("/run-benchmarks", summary="Execute Full Scenario Benchmark Suite")
def run_all_benchmarks(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission(Permission.SIMULATE)),
):
    """Executes all 10+ benchmark scenarios and returns aggregate metrics."""
    return system_evaluator.evaluate_all_scenarios()


@router.get("/performance", summary="Get Endpoint Performance Latency Benchmarks")
def get_performance_benchmarks(auth: AuthContext = Depends(require_permission(Permission.VIEW))):
    """Returns empirical latency benchmarks across endpoints (p50, p95, p99, error rate)."""
    return performance_benchmarker.get_benchmark_results()


@router.get("/memory-metrics", summary="Get Hindsight Memory Quality Metrics")
def get_memory_quality_metrics(auth: AuthContext = Depends(require_permission(Permission.VIEW))):
    """Returns verified memory quality metrics including recall relevance and mistake avoidance."""
    return MemoryQualityMetrics().model_dump()


@router.post("/chaos/inject", summary="Inject Synthetic Chaos Telemetry")
def inject_chaos(
    payload: ChaosInjectionRequest,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission(Permission.SIMULATE)),
):
    """Injects synthetic failure signals strictly into the chaos sandbox."""
    org_id = uuid.UUID(payload.organization_id) if payload.organization_id else None
    return chaos_injector.inject(scenario_id=payload.scenario_id, db=db, organization_id=org_id)


@router.post("/chaos/run", summary="Execute Complete Chaos Mitigation Loop")
def run_chaos_mitigation(
    payload: ChaosInjectionRequest,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission(Permission.SIMULATE)),
):
    """Executes the full 10-step cognitive loop against an injected chaos scenario."""
    org_id = uuid.UUID(payload.organization_id) if payload.organization_id else None
    return chaos_runner.run_chaos_test(scenario_id=payload.scenario_id, db=db, organization_id=org_id)
