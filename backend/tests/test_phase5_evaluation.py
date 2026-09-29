"""Phase 5 Evaluation & Benchmarking Tests for NEXUS-Ω."""

import uuid
import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.main import app
from app.evaluation.scenarios import BENCHMARK_SCENARIOS
from app.evaluation.memory_ablation import memory_ablation_engine
from app.evaluation.evaluator import system_evaluator
from app.evaluation.metrics import MemoryInfluenceScore
from app.evaluation.reports import report_generator


@pytest.fixture
def client():
    return TestClient(app)


def test_scenario_catalog_integrity():
    """Verifies that at least 10 realistic organizational scenarios exist with distinct answers."""
    assert len(BENCHMARK_SCENARIOS) >= 10
    scenario_ids = [s.id for s in BENCHMARK_SCENARIOS]
    assert len(scenario_ids) == len(set(scenario_ids)), "Scenario IDs must be unique"

    optimal_actions = set(s.expected_optimal_action for s in BENCHMARK_SCENARIOS)
    assert len(optimal_actions) >= 8, "Scenarios must not all have the same answer"

    for scenario in BENCHMARK_SCENARIOS:
        assert scenario.current_incident
        assert len(scenario.historical_experiences) >= 2
        assert scenario.expected_challenge
        assert scenario.context_trap


def test_memory_ablation_mode_a_vs_mode_b():
    """Verifies that running without memory falls into failure trap, while with Hindsight succeeds."""
    result = memory_ablation_engine.run_ablation("scenario-01-payment-failure")

    without_mem = result["without_memory"]
    with_mem = result["with_memory"]

    # Mode A (Without Memory)
    assert without_mem["evidence_retrieved_count"] == 0
    assert without_mem["repeated_mistake_detected"] is False
    assert without_mem["recommendation"] == "restart_gateway"
    assert without_mem["calibrated_confidence"] < 0.70

    # Mode B (With Hindsight)
    assert with_mem["evidence_retrieved_count"] > 0
    assert with_mem["repeated_mistake_detected"] is True
    assert with_mem["repeated_mistake_prevented"] is True
    assert with_mem["recommendation"] == "switch_secondary_rail_b"
    assert with_mem["calibrated_confidence"] > 0.90

    # Verify differences and memory influence
    assert len(result["differences"]) >= 4
    influence = result["memory_influence"]
    assert influence["score"] > 0.70
    assert influence["level"] in ["HIGH", "DECISIVE"]
    assert "prevented historical failure" in influence["explanation"].lower()


def test_difficult_memory_context_scenario():
    """Verifies that the system discriminates context rather than naively choosing the newest memory."""
    scenario = next(s for s in BENCHMARK_SCENARIOS if s.id == "scenario-diff-01-context-nuance")
    result = memory_ablation_engine.run_ablation(scenario.id)

    # In sustained provider outage, restart is known to fail
    assert result["with_memory"]["repeated_mistake_prevented"] is True
    assert result["with_memory"]["recommendation"] == "switch_to_secondary_provider_b"
    assert "provider" in result["with_memory"]["recommendation_rationale"].lower()


def test_contradictory_memory_scenario():
    """Verifies that the system detects contradiction between outdated and current guidelines."""
    scenario = next(s for s in BENCHMARK_SCENARIOS if s.id == "scenario-conf-01-contradictory")
    result = memory_ablation_engine.run_ablation(scenario.id)

    assert result["with_memory"]["contradiction_detected"] is True
    assert result["with_memory"]["recommendation"] == "distribute_multi_zone_mesh"


def test_system_evaluator_all_scenarios():
    """Runs the entire scenario benchmark suite and computes aggregate metrics."""
    eval_result = system_evaluator.evaluate_all_scenarios()

    summary = eval_result["summary"]
    assert summary["total_scenarios_evaluated"] >= 10
    assert summary["mistake_prevention_rate_pct"] == 100.0
    assert summary["average_memory_influence_score"] > 0.50
    assert summary["contradiction_handling_verified"] is True
    assert summary["context_discrimination_verified"] is True


def test_report_generator_and_export():
    """Verifies machine-readable evaluation report generation without fake data."""
    report = report_generator.generate_full_report()
    assert report["title"] == "NEXUS-Ω System-Wide Evaluation Report"
    assert "benchmark_summary" in report
    assert "performance_benchmarks" in report
    assert "memory_quality_metrics" in report
    assert "causal_metrics" in report
    assert "counterfactual_metrics" in report
    assert "safety_and_access_control" in report


def test_phase5_api_endpoints(client):
    """Verifies all Phase 5 API endpoints responding with real data."""
    # 1. Memory Ablation API
    ablate_resp = client.post(
        "/evaluation/memory-ablation",
        json={"scenario_id": "scenario-01-payment-failure"},
    )
    assert ablate_resp.status_code == 200
    data = ablate_resp.json()
    assert "without_memory" in data
    assert "with_memory" in data
    assert "differences" in data
    assert "memory_influence" in data

    # 2. Benchmark Suite API
    bench_resp = client.post("/evaluation/run-benchmarks")
    assert bench_resp.status_code == 200
    bench_data = bench_resp.json()
    assert bench_data["summary"]["total_scenarios_evaluated"] >= 10

    # 3. Performance API
    perf_resp = client.get("/evaluation/performance")
    assert perf_resp.status_code == 200
    perf_data = perf_resp.json()
    assert "endpoints" in perf_data
    assert "/memory/search" in perf_data["endpoints"]
    assert "/causal/root-cause" in perf_data["endpoints"]

    # 4. Memory Metrics API
    mem_resp = client.get("/evaluation/memory-metrics")
    assert mem_resp.status_code == 200
    mem_data = mem_resp.json()
    assert mem_data["recall_relevance_p90"] > 0.90
    assert mem_data["hallucination_rate_with_hindsight"] < 0.05

    # 5. System Readiness Probe
    ready_resp = client.get("/system/readiness")
    assert ready_resp.status_code == 200
    ready_data = ready_resp.json()
    assert "engines" in ready_data
    assert "postgresql" in ready_data["engines"]
    assert "hindsight" in ready_data["engines"]
    assert "causal_engine" in ready_data["engines"]

    # 6. Decision Trace Endpoint
    trace_resp = client.get("/decisions/mock-decision-id/trace")
    assert trace_resp.status_code == 200
    trace_data = trace_resp.json()
    assert "problem" in trace_data
    assert "memories" in trace_data
    assert "causal_evidence" in trace_data
    assert "simulations" in trace_data
    assert "reflection" in trace_data

    # 7. Investigation Replay Endpoint
    replay_resp = client.get("/investigations/replay/mock-request-id")
    assert replay_resp.status_code == 200
    replay_data = replay_resp.json()
    assert "agent_outputs" in replay_data or "agent_runs" in replay_data

    # 8. Demo Reset Endpoint
    reset_resp = client.post("/demo/reset")
    assert reset_resp.status_code == 200
    assert reset_resp.json()["status"] == "reset_successful"
