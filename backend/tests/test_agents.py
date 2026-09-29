"""Comprehensive Unit and Integration Tests for NEXUS-Ω Multi-Agent System."""

import uuid
import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.models import Organization, Customer, Experience, Decision
from app.agents.state import AgentState, MemoryItem, MemoryConflict
from app.agents.planner_agent import planner_agent
from app.agents.memory_agent import memory_agent, MemoryConflictDetector
from app.agents.analyst_agent import analyst_agent
from app.agents.causal_agent import causal_agent
from app.agents.risk_agent import risk_agent
from app.agents.decision_agent import decision_agent
from app.agents.critic_agent import critic_agent
from app.agents.reflection_agent import reflection_agent
from app.agents.orchestrator import orchestrator


@pytest.fixture
def agent_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSession()

    org = Organization(name="Agent Test Corp")
    session.add(org)
    session.commit()
    session.refresh(org)

    cust = Customer(
        organization_id=org.id,
        name="ACME Corp",
        industry="E-commerce",
        status="active",
        risk_level="high",
    )
    session.add(cust)

    exp1 = Experience(
        organization_id=org.id,
        experience_type="incident_resolution",
        description="ACME payment gateway timeout failure #1 resolved by retry.",
        action_taken="Payment gateway connection retry",
        outcome="Gateway connection recovered",
        success=True,
        hindsight_bank_id="nexus-demo",
    )
    exp2 = Experience(
        organization_id=org.id,
        experience_type="incident_resolution",
        description="ACME payment gateway timeout failure #3 required gateway switch.",
        action_taken="Switched payment traffic to secondary gateway rail",
        outcome="Payment success rate immediately recovered to 99.98%",
        success=True,
        hindsight_bank_id="nexus-demo",
    )
    exp_fail = Experience(
        organization_id=org.id,
        experience_type="operational_mistake",
        description="Payment service restarted under connection pool leak.",
        action_taken="Restart the payment service",
        outcome="Restart failed to resolve pool leak; failure returned after 20 minutes.",
        success=False,
        hindsight_bank_id="nexus-demo",
    )
    session.add_all([exp1, exp2, exp_fail])
    session.commit()

    yield session, org

    session.close()


def test_planner_agent(agent_db):
    session, org = agent_db
    state = AgentState(
        organization_id=org.id,
        user_request="ACME is experiencing payment failures again. Investigate and recommend actions.",
    )
    state = planner_agent.execute(state, session)
    assert len(state.timeline) == 1
    assert state.timeline[0].agent == "PlannerAgent"
    assert "plan_steps" in state.planner_output
    assert len(state.planner_output["plan_steps"]) == 9
    assert "MemoryAgent" in state.planner_output["required_agents"]


def test_memory_conflict_detector():
    memories = [
        MemoryItem(
            memory_id="m1",
            summary="Payment gateway connection retry succeeded on transient timeouts.",
            outcome="Recovered connection",
        ),
        MemoryItem(
            memory_id="m2",
            summary="Payment gateway connection retry failed during complete vendor outage causing severe backlog.",
            outcome="Failed",
        ),
    ]
    conflicts = MemoryConflictDetector.detect_conflicts(memories)
    assert len(conflicts) == 1
    assert conflicts[0].conflict is True
    assert conflicts[0].resolution_strategy == "requires_context"
    assert "nuance" in conflicts[0].explanation


def test_memory_agent(agent_db):
    session, org = agent_db
    state = AgentState(
        organization_id=org.id,
        user_request="ACME payment failure history",
    )
    with patch("app.services.memory_service.memory_service.recall_memories") as mock_recall:
        mock_recall.return_value = [
            {"id": "h1", "text": "ACME payment gateway failure resolved by retry", "metadata": {}, "tags": ["incident"]}
        ]
        state = memory_agent.execute(state, session)
        assert len(state.recalled_memories) > 0
        assert any(m.source == "hindsight_bank" for m in state.recalled_memories)
        assert any(m.source == "postgresql_experiences" for m in state.recalled_memories)


def test_analyst_agent(agent_db):
    session, org = agent_db
    state = AgentState(
        organization_id=org.id,
        user_request="Investigate ACME payment degradation",
        recalled_memories=[
            MemoryItem(memory_id="1", summary="ACME payment gateway timeout recurring", outcome="Resolved by switch")
        ],
    )
    state = analyst_agent.execute(state, session)
    assert "patterns" in state.analyst_output
    assert len(state.analyst_output["patterns"]) > 0
    assert len(state.analyst_output["historical_comparisons"]) > 0


def test_causal_agent(agent_db):
    session, org = agent_db
    state = AgentState(
        organization_id=org.id,
        user_request="ACME payment failures and restarts",
        recalled_memories=[
            MemoryItem(memory_id="1", summary="Payment gateway connection timeout causes payment failures.", outcome="Resolved by retry"),
            MemoryItem(memory_id="2", summary="Restarting payment service failed because of connection pool leak.", outcome="Failed after 20 minutes"),
        ],
    )
    state = causal_agent.execute(state, session)
    relationships = state.causal_output.get("relationships", [])
    assert len(relationships) >= 2
    rel_types = [r["relationship"] for r in relationships]
    assert "CAUSES" in rel_types or "RESOLVED_BY" in rel_types


def test_risk_agent(agent_db):
    session, org = agent_db
    state = AgentState(
        organization_id=org.id,
        user_request="ACME payment failures and proposed restart",
        causal_output={"relationships": [{"source_event": "restart", "relationship": "CONTRADICTS"}]},
    )
    state = risk_agent.execute(state, session)
    risks = state.risk_output.get("risks", [])
    assert len(risks) > 0
    assert state.risk_output["severity"] in ["medium", "high", "critical"]
    risk_types = [r["risk_type"] for r in risks]
    assert "customer_impact" in risk_types or "historical_failure_risk" in risk_types


def test_decision_agent(agent_db):
    session, org = agent_db
    state = AgentState(
        organization_id=org.id,
        user_request="ACME payment failure recommendation",
    )
    state = decision_agent.execute(state, session)
    candidates = state.decision_output.get("candidates", [])
    assert len(candidates) >= 2
    primary = state.decision_output.get("primary_decision", {})
    assert "action" in primary
    assert primary.get("approval_required") is True


def test_critic_agent(agent_db):
    session, org = agent_db
    state = AgentState(
        organization_id=org.id,
        user_request="ACME payment failure with proposed restart",
        decision_output={
            "primary_decision": {
                "action": "Switch ACME transaction traffic to Secondary Payment Gateway Rail B",
                "rationale_summary": "Gateway switching succeeded in previous incident",
                "expected_outcome": "Immediate recovery",
            }
        },
        recalled_memories=[
            MemoryItem(memory_id="1", summary="ACME payment gateway switch succeeded", outcome="Success"),
        ],
    )
    state = critic_agent.execute(state, session)
    assert state.final_recommendation is not None
    assert "RECOMMENDED ACTION" in state.final_recommendation
    assert state.provenance is not None
    assert len(state.provenance.evidence_items) > 0


def test_reflection_agent(agent_db):
    session, org = agent_db
    state = AgentState(
        organization_id=org.id,
        user_request="ACME payment failure resolution",
        decision_output={
            "primary_decision": {
                "action": "Switch to Secondary Gateway Rail B",
                "expected_outcome": "Recovery to 99.98%",
            }
        },
    )
    with patch("app.services.memory_service.memory_service.retain_experience") as mock_retain:
        mock_retain.return_value = {"success": True}
        state = reflection_agent.execute(state, session)
        assert state.reflection_result is not None
        assert "lessons_learned" in state.reflection_result


def test_orchestrator_complete_e2e_investigation(agent_db):
    session, org = agent_db
    user_request = (
        "ACME is experiencing payment failures again. Investigate what happened historically, "
        "identify what caused previous failures, determine what worked and what failed, "
        "evaluate the current situation, and recommend the next action."
    )

    with patch("app.services.memory_service.memory_service.recall_memories") as mock_recall, \
         patch("app.services.memory_service.memory_service.retain_experience") as mock_retain:
        mock_recall.return_value = [
            {"id": "h1", "text": "Customer ACME Corp experienced three payment failures. First two resolved by retry, third by gateway switch.", "metadata": {}, "tags": ["incident"]},
            {"id": "h2", "text": "Restarting payment service failed to resolve connection pool leak; failure returned after 20 minutes.", "metadata": {}, "tags": ["failure"]},
            {"id": "h3", "text": "Generic automated communication caused customer escalation with ACME Corp.", "metadata": {}, "tags": ["communication"]},
        ]
        mock_retain.return_value = {"success": True}

        state = orchestrator.run_investigation(
            db=session,
            organization_id=org.id,
            user_request=user_request,
            user_id="user-qa-01",
        )

        assert state.status == "completed"
        # 8 distinct agents executed in timeline
        assert len(state.timeline) == 8
        agent_names = [t.agent for t in state.timeline]
        assert agent_names == [
            "PlannerAgent",
            "MemoryAgent",
            "AnalystAgent",
            "CausalAgent",
            "DecisionAgent",
            "RiskAgent",
            "CriticAgent",
            "ReflectionAgent",
        ]
        assert state.final_recommendation is not None
        assert "Switch" in state.final_recommendation
        assert state.approval_required is True
        assert state.provenance is not None
        assert len(state.provenance.evidence_items) > 0


def test_api_investigate_endpoint(agent_db):
    from fastapi.testclient import TestClient
    from app.main import app
    from app.db.database import get_db

    session, org = agent_db
    app.dependency_overrides[get_db] = lambda: session
    client = TestClient(app)

    payload = {
        "organization_id": str(org.id),
        "request": "ACME is experiencing payment failures again.",
        "user_id": "test-user-01",
    }

    try:
        with patch("app.services.memory_service.memory_service.recall_memories") as mock_recall, \
             patch("app.services.memory_service.memory_service.retain_experience") as mock_retain:
            mock_recall.return_value = [
                {"id": "h1", "text": "Customer ACME Corp payment failures were resolved by gateway switch.", "metadata": {}, "tags": ["incident"]}
            ]
            mock_retain.return_value = {"success": True}

            response = client.post("/agents/investigate", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "completed"
            assert len(data["timeline"]) == 8
            assert "plan" in data
            assert "causal_analysis" in data
            assert "risks" in data
            assert "final_recommendation" in data
            assert data["approval_required"] is True
            assert data["provenance"] is not None
    finally:
        app.dependency_overrides.pop(get_db, None)
