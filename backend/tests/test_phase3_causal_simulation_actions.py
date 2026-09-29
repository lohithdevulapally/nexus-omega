"""Phase 3 Test Suite: Causal Intelligence, Counterfactual Simulation, and Controlled Action Engine."""

import uuid
from datetime import datetime, timezone
from unittest.mock import patch
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.models import Organization, Customer, Event, Experience, Action
from app.causal.nodes import CausalEntityType, CausalNodeDTO
from app.causal.edges import CausalRelationshipType, CausalEdgeDTO
from app.causal.causal_store import causal_store
from app.causal.graph import CausalKnowledgeGraph
from app.causal.inference import causal_inference
from app.causal.confidence import CausalConfidenceCalculator
from app.causal.causal_engine import causal_engine, CausalEvidenceEngine, CausalConflictDetector
from app.simulation.state_snapshot import StateSnapshot
from app.simulation.scenarios import ScenarioBuilder
from app.simulation.evaluator import CounterfactualEvaluator
from app.simulation.simulator import counterfactual_engine
from app.actions.action_registry import ActionRegistry, ActionType, ActionRiskTier
from app.actions.validators import ActionValidator, ActionValidationError
from app.actions.approval import HumanApprovalSystem
from app.actions.executor import ActionExecutor
from app.actions.action_engine import action_engine
from app.agents.orchestrator import orchestrator
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_db

from sqlalchemy.pool import StaticPool

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def p3_db():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    org = Organization(
        id=uuid.uuid4(),
        name="Cyberdyne Systems",
        created_at=datetime.now(timezone.utc),
    )
    session.add(org)

    cust = Customer(
        id=uuid.uuid4(),
        organization_id=org.id,
        name="Skynet R&D",
        industry="Defense",
        status="active",
        risk_level="high",
        created_at=datetime.now(timezone.utc),
    )
    session.add(cust)

    exp = Experience(
        id=uuid.uuid4(),
        organization_id=org.id,
        experience_type="incident",
        description="Payment gateway timeout under sustained load resolved when switched to secondary rail B.",
        action_taken="Switched to Secondary Rail B",
        outcome="Restored payment processing within 60 seconds.",
        success=True,
        hindsight_bank_id="nexus-demo",
        created_at=datetime.now(timezone.utc),
    )
    session.add(exp)

    ev = Event(
        id=uuid.uuid4(),
        organization_id=org.id,
        title="Payment Gateway Timeout",
        event_type="failure",
        entity_id="Skynet R&D",
        metadata_json={"severity": "critical"},
        created_at=datetime.now(timezone.utc),
    )
    session.add(ev)
    session.commit()

    yield session, org

    session.close()
    Base.metadata.drop_all(bind=engine)


# 1. Causal Node & Edge Creation
def test_causal_node_and_edge_creation(p3_db):
    session, org = p3_db
    node_a = causal_store.get_or_create_node(
        db=session,
        organization_id=org.id,
        label="Gateway Latency Spike",
        entity_type=CausalEntityType.FAILURE.value,
    )
    node_b = causal_store.get_or_create_node(
        db=session,
        organization_id=org.id,
        label="Payment Timeout Event",
        entity_type=CausalEntityType.INCIDENT.value,
    )
    assert node_a.label == "Gateway Latency Spike"
    assert node_b.label == "Payment Timeout Event"

    edge = causal_store.add_or_update_edge(
        db=session,
        organization_id=org.id,
        source_node_id=node_a.id,
        target_node_id=node_b.id,
        relationship=CausalRelationshipType.CAUSES.value,
        confidence=0.95,
        evidence={"observed": True},
    )
    assert edge.relationship == "CAUSES"
    assert edge.confidence == 0.95


# 2. Causal Evidence Collection & Confidence
def test_causal_evidence_and_confidence(p3_db):
    session, org = p3_db
    with patch("app.services.memory_service.memory_service.recall_memories") as mock_recall:
        mock_recall.return_value = [{"text": "Switching rail resolved payment gateway timeout."}]

        ev = CausalEvidenceEngine.collect_evidence(
            db=session,
            organization_id=org.id,
            source_label="Payment gateway timeout",
            target_label="secondary rail",
            relationship="RESOLVED_BY",
        )
        assert ev["confidence"] >= 0.85
        assert len(ev["supporting_events"]) > 0 or len(ev["supporting_memories"]) > 0

    # Ensure correlation does not get artificially high confidence
    corr_conf = CausalConfidenceCalculator.calculate_confidence(
        relationship="CORRELATED_WITH",
        supporting_events=[1, 2, 3],
        supporting_memories=[],
        counter_evidence=[],
    )
    assert corr_conf <= 0.65


# 3. Causal Conflict Detection
def test_causal_conflict_detection():
    candidate = {"source": "Gateway Restart", "target": "Incident Resolution", "relationship": "RESOLVED_BY"}
    existing = [{"source": "Gateway Restart", "target": "Incident Resolution", "relationship": "FAILED_BECAUSE_OF", "evidence": {}}]

    res = CausalConflictDetector.detect_conflicts(candidate, existing)
    assert res["conflict"] is True
    assert res["resolution_status"] == "context_dependent"
    assert len(res["competing_hypotheses"]) == 2


# 4. Root Cause Analysis
def test_root_cause_analysis(p3_db):
    session, org = p3_db
    graph = CausalKnowledgeGraph(organization_id=str(org.id))

    # Construct causal chain: Upstream Network Outage -> CAUSES -> Gateway Timeout -> TRIGGERS -> Payment Failures
    n1 = graph.add_node(CausalNodeDTO(organization_id=str(org.id), entity_type="Failure", label="Upstream Network Outage"))
    n2 = graph.add_node(CausalNodeDTO(organization_id=str(org.id), entity_type="Incident", label="Gateway Timeout"))
    n3 = graph.add_node(CausalNodeDTO(organization_id=str(org.id), entity_type="Incident", label="Payment Failures"))

    graph.add_edge(CausalEdgeDTO(organization_id=str(org.id), source_node_id=n1.id, target_node_id=n2.id, relationship="CAUSES", confidence=0.95))
    graph.add_edge(CausalEdgeDTO(organization_id=str(org.id), source_node_id=n2.id, target_node_id=n3.id, relationship="TRIGGERS", confidence=0.90))

    rc = causal_inference.analyze_root_cause(graph, "Payment Failures", depth=5)
    assert rc["incident"] == "Payment Failures"
    assert len(rc["upstream_causes"]) >= 1
    assert rc["immediate_cause"] is not None


# 5. Causal Path Traversal & Cascade Analysis
def test_causal_path_and_cascade(p3_db):
    session, org = p3_db
    graph = CausalKnowledgeGraph(organization_id=str(org.id))

    n1 = graph.add_node(CausalNodeDTO(organization_id=str(org.id), entity_type="Failure", label="Primary Timeout"))
    n2 = graph.add_node(CausalNodeDTO(organization_id=str(org.id), entity_type="Incident", label="Transaction Queue Growth"))
    n3 = graph.add_node(CausalNodeDTO(organization_id=str(org.id), entity_type="Risk", label="Executive Outage Escalation"))

    graph.add_edge(CausalEdgeDTO(organization_id=str(org.id), source_node_id=n1.id, target_node_id=n2.id, relationship="CAUSES", confidence=0.92))
    graph.add_edge(CausalEdgeDTO(organization_id=str(org.id), source_node_id=n2.id, target_node_id=n3.id, relationship="AMPLIFIES", confidence=0.88))

    paths = causal_inference.find_paths(graph, "Primary Timeout", "Executive Outage Escalation")
    assert paths["path_count"] == 1
    assert paths["paths"][0]["path_length"] == 2

    cascade = causal_inference.analyze_cascade(graph, "Primary Timeout", depth=3)
    assert cascade["total_downstream_entities"] == 2
    assert cascade["severity"] in ["medium", "high", "critical"]


# 6. State Snapshot & Simulation Isolation
def test_state_snapshot_isolation(p3_db):
    session, org = p3_db
    snap = StateSnapshot.capture(session, org.id, source_request="Test verification")
    assert snap.simulation_tag == "SIMULATION_ONLY"
    assert len(snap.customers) == 1
    assert len(snap.events) == 1
    assert snap.state_hash is not None

    # Verify simulation actions do not mutate PostgreSQL state
    initial_event_count = len(session.query(Event).all())
    graph = CausalKnowledgeGraph(organization_id=str(org.id))
    sim_res = counterfactual_engine.simulate_action("Restart Gateway A", snap, graph)

    assert sim_res.simulation_id.startswith("sim-")
    assert len(sim_res.projected_outcomes) > 0
    assert len(session.query(Event).all()) == initial_event_count  # No production mutation!


# 7. Counterfactual Dual-World Comparison
def test_counterfactual_engine(p3_db):
    session, org = p3_db
    with patch("app.services.memory_service.memory_service.recall_memories") as mock_recall:
        mock_recall.return_value = [{"text": "Gateway restart failed repeatedly under high concurrency."}]

        delta = counterfactual_engine.run_counterfactual(
            db=session,
            organization_id=org.id,
            incident_id="Payment Gateway Degradation",
            alternative_action="restart_gateway",
            baseline_action="switch_to_secondary_rail_b",
        )

        assert "actual_world" in delta
        assert "counterfactual_world" in delta
        assert len(delta["differences"]) > 0
        assert delta["confidence"] >= 0.80


# 8. Multi-Scenario Comparison
def test_multi_scenario_comparison(p3_db):
    session, org = p3_db
    with patch("app.services.memory_service.memory_service.recall_memories") as mock_recall:
        mock_recall.return_value = [{"text": "Switching rail succeeded in Incident #3."}]

        comp = counterfactual_engine.compare_scenarios(
            db=session,
            organization_id=org.id,
            decision_context="ACME Payment Timeout",
            options=["switch_to_secondary_rail", "restart_gateway", "wait_and_monitor"],
        )

        assert len(comp.options_evaluated) == 3
        options = [o.option for o in comp.options_evaluated]
        assert "switch_to_secondary_rail" in options
        assert "restart_gateway" in options
        assert "wait_and_monitor" in options


# 9. Historical State Reconstruction (Time-Travel)
def test_historical_state_reconstruction(p3_db):
    session, org = p3_db
    target_time = datetime.now(timezone.utc).isoformat()
    reconstruction = counterfactual_engine.reconstruct_historical_state(
        db=session,
        organization_id=org.id,
        timestamp_iso=target_time,
    )
    assert reconstruction["simulation_tag"] == "SIMULATION_ONLY"
    assert "entities" in reconstruction
    assert "events" in reconstruction


# 10. Action Registry & Validation
def test_action_validation():
    # Valid low risk action
    valid = ActionValidator.validate_request(
        action_type=ActionType.CREATE_INTERNAL_EVENT.value,
        parameters={"title": "Audit Check", "event_type": "audit"},
    )
    assert valid["valid"] is True
    assert valid["requires_human_approval"] is False

    # Blocked shell command
    with pytest.raises(ActionValidationError):
        ActionValidator.validate_request(
            action_type=ActionType.CREATE_INTERNAL_EVENT.value,
            parameters={"title": "echo rm -rf ; drop table", "event_type": "audit"},
        )

    # Disallowed arbitrary action
    with pytest.raises(ActionValidationError):
        ActionValidator.validate_request(
            action_type="execute_bash_command",
            parameters={"cmd": "ls"},
        )


# 11. Action Approval Workflow & Execution
def test_action_approval_and_execution(p3_db):
    session, org = p3_db

    # 1. Request high-impact action (send_webhook requires approval)
    action = action_engine.request_action(
        db=session,
        organization_id=org.id,
        action_type=ActionType.SEND_WEBHOOK.value,
        parameters={"endpoint_url": "https://hooks.internal.net/alert", "payload": {"status": "urgent"}},
        requested_by="decision_agent",
    )
    assert action.approval_required is True
    assert action.approval_status == "pending"

    # Execution before approval should fail
    with pytest.raises(ActionValidationError):
        action_engine.execute_action(db=session, action_id=action.id)

    # 2. Approve action
    approved = action_engine.approve_action(
        db=session,
        action_id=action.id,
        approved_by="lead_sre_operator",
        comment="Approved following canary validation.",
    )
    assert approved.approval_status == "approved"

    # 3. Execute approved action
    executed = action_engine.execute_action(db=session, action_id=action.id, executed_by="lead_sre_operator")
    assert executed.status == "executed"
    assert executed.execution_status == "completed"
    assert executed.result is not None


# 12. Full Decision -> Simulation -> Approval -> Action Loop
def test_full_decision_simulation_action_loop(p3_db):
    session, org = p3_db
    user_request = "ACME is experiencing payment failures again. Evaluate options, simulate what happens, and recommend action."

    with patch("app.services.memory_service.memory_service.recall_memories") as mock_recall, \
         patch("app.services.memory_service.memory_service.retain_experience") as mock_retain:
        mock_recall.return_value = [
            {"id": "h1", "text": "Customer ACME Corp experienced payment failure. Switched to rail B with 99.98% recovery.", "metadata": {}, "tags": ["incident"]},
            {"id": "h2", "text": "Restarting payment service failed; failure returned after 20 minutes.", "metadata": {}, "tags": ["failure"]},
        ]
        mock_retain.return_value = {"success": True}

        state = orchestrator.run_investigation(
            db=session,
            organization_id=org.id,
            user_request=user_request,
            user_id="lead-sre",
        )

        assert state.status == "completed"
        # Simulation output attached
        assert state.simulation_output is not None
        # Action was registered
        assert state.action_id is not None
        assert state.approval_required is True
        assert state.final_recommendation is not None


# 13. API Integration Tests for Causal, Simulation, and Actions
def test_phase3_api_endpoints(p3_db):
    session, org = p3_db
    app.dependency_overrides[get_db] = lambda: session
    client = TestClient(app)

    try:
        # Seed graph in session
        causal_engine.seed_default_graph(session, org.id)

        # A. Causal Root Cause API
        rc_resp = client.post(
            "/causal/root-cause",
            json={"organization_id": str(org.id), "incident_id": "ACME Transaction Failures", "depth": 5},
        )
        assert rc_resp.status_code == 200
        rc_data = rc_resp.json()
        assert rc_data["incident"] == "ACME Transaction Failures"
        assert len(rc_data["upstream_causes"]) > 0

        # B. Causal Path API
        path_resp = client.get(
            f"/causal/path?source=Payment+Gateway+Connection+Timeout&target=ACME+Executive+Escalation&organization_id={str(org.id)}"
        )
        assert path_resp.status_code == 200
        path_data = path_resp.json()
        assert path_data["path_count"] >= 1

        # C. Causal Cascade API
        cascade_resp = client.post(
            "/causal/cascade",
            json={"organization_id": str(org.id), "trigger": "Payment Gateway Connection Timeout", "depth": 5},
        )
        assert cascade_resp.status_code == 200
        cascade_data = cascade_resp.json()
        assert cascade_data["total_downstream_entities"] > 0

        # D. Counterfactual API
        with patch("app.services.memory_service.memory_service.recall_memories") as mock_recall:
            mock_recall.return_value = [{"text": "Gateway restart failed repeatedly."}]
            cf_resp = client.post(
                "/simulation/counterfactual",
                json={
                    "organization_id": str(org.id),
                    "incident_id": "Payment Gateway Connection Timeout",
                    "alternative_action": "restart_gateway",
                },
            )
            assert cf_resp.status_code == 200
            cf_data = cf_resp.json()
            assert "actual_world" in cf_data
            assert "counterfactual_world" in cf_data
            assert len(cf_data["differences"]) > 0

        # E. Compare Scenarios API
        with patch("app.services.memory_service.memory_service.recall_memories") as mock_recall:
            mock_recall.return_value = [{"text": "Switching rail succeeded in Incident #3."}]
            cmp_resp = client.post(
                "/simulation/compare",
                json={
                    "organization_id": str(org.id),
                    "decision_context": "ACME Payment Timeout",
                    "options": ["switch_to_secondary_rail", "restart_gateway", "wait_and_monitor"],
                },
            )
            assert cmp_resp.status_code == 200
            cmp_data = cmp_resp.json()
            assert len(cmp_data["options_evaluated"]) == 3

        # F. Reconstruct Historical State API
        reconstruct_resp = client.post(
            "/simulation/reconstruct",
            json={"organization_id": str(org.id), "timestamp": datetime.now(timezone.utc).isoformat()},
        )
        assert reconstruct_resp.status_code == 200
        reconstruct_data = reconstruct_resp.json()
        assert reconstruct_data["simulation_tag"] == "SIMULATION_ONLY"

        # G. Actions API: Submit, Approve, Execute
        act_resp = client.post(
            "/actions",
            json={
                "organization_id": str(org.id),
                "action_type": "update_customer_status",
                "parameters": {"customer_id": str(session.query(Customer).first().id), "status": "active", "risk_level": "medium"},
                "requested_by": "qa_operator",
            },
        )
        assert act_resp.status_code == 200
        act_data = act_resp.json()
        action_id = act_data["id"]
        assert act_data["approval_required"] is True
        assert act_data["approval_status"] == "pending"

        # Approve
        appr_resp = client.post(
            f"/actions/{action_id}/approve",
            json={"approved_by": "lead_engineer", "comment": "Approved for testing"},
        )
        assert appr_resp.status_code == 200
        assert appr_resp.json()["approval_status"] == "approved"

        # Execute
        exec_resp = client.post(
            f"/actions/{action_id}/execute",
            json={"executed_by": "lead_engineer"},
        )
        assert exec_resp.status_code == 200
        assert exec_resp.json()["status"] == "executed"
        assert exec_resp.json()["result"]["updated"] is True

    finally:
        app.dependency_overrides.pop(get_db, None)
