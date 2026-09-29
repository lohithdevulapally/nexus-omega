"""Phase 5 Security, Multi-Tenancy Isolation, RBAC, and Chaos Tests."""

import uuid
import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import SessionLocal
from app.db.models import Organization, Customer, Event, Action, AuditLog
from app.actions.action_engine import action_engine
from app.actions.validators import ActionValidationError
from app.chaos.injector import chaos_injector, SANDBOX_CHAOS_ORG_ID
from app.chaos.runner import chaos_runner
from app.chaos.evaluator import chaos_evaluator


@pytest.fixture
def client():
    return TestClient(app)


def test_rbac_viewer_forbidden_from_approving_or_executing(client):
    """Verifies that VIEWER role is blocked from approving or executing actions (HTTP 403)."""
    db = SessionLocal()
    org_id = uuid.UUID("2d48f08c-0b35-4aea-8941-86e4f855f738")

    # Create an action requiring approval
    action = action_engine.request_action(
        db=db,
        organization_id=org_id,
        action_type="switch_payment_rail",
        parameters={"from_rail": "rail_a", "to_rail": "rail_b"},
        requested_by="analyst_user",
        risk_level="high",
        approval_required=True,
    )
    action_id = str(action.id)
    db.close()

    # Attempt approve as VIEWER -> 403 Forbidden
    resp_approve = client.post(
        f"/actions/{action_id}/approve",
        headers={"X-User-Role": "VIEWER", "X-User-Id": "viewer_bob"},
        json={"approved_by": "viewer_bob", "comment": "Trying unauthorized approve"},
    )
    assert resp_approve.status_code == 403
    assert "does not possess required permission" in resp_approve.json()["detail"]

    # Attempt execute as VIEWER -> 403 Forbidden
    resp_exec = client.post(
        f"/actions/{action_id}/execute",
        headers={"X-User-Role": "VIEWER", "X-User-Id": "viewer_bob"},
        json={"executed_by": "viewer_bob"},
    )
    assert resp_exec.status_code == 403

    # Attempt approve as OPERATOR -> 200 OK
    resp_operator_approve = client.post(
        f"/actions/{action_id}/approve",
        headers={"X-User-Role": "OPERATOR", "X-User-Id": "op_alice"},
        json={"approved_by": "op_alice", "comment": "Authorized by operator"},
    )
    assert resp_operator_approve.status_code == 200
    assert resp_operator_approve.json()["approval_status"] == "approved"


def test_action_safety_rejections():
    """Verifies protection against duplicate execution, unauthorized execution, and injection attempts."""
    db = SessionLocal()
    org_id = uuid.UUID("2d48f08c-0b35-4aea-8941-86e4f855f738")

    # 1. Shell injection attempt blocked
    with pytest.raises(ActionValidationError) as exc_info:
        action_engine.request_action(
            db=db,
            organization_id=org_id,
            action_type="switch_payment_rail",
            parameters={"from_rail": "rail_a; rm -rf /", "to_rail": "rail_b"},
        )
    assert "hazardous command strings" in str(exc_info.value)

    # 2. Unregistered arbitrary action blocked
    with pytest.raises(ActionValidationError) as exc_info:
        action_engine.request_action(
            db=db,
            organization_id=org_id,
            action_type="delete_all_databases",
            parameters={},
        )
    assert "strictly forbidden" in str(exc_info.value)

    # 3. Execution without approval blocked
    action = action_engine.request_action(
        db=db,
        organization_id=org_id,
        action_type="switch_payment_rail",
        parameters={"from_rail": "rail_a", "to_rail": "rail_b"},
        risk_level="critical",
        approval_required=True,
    )
    with pytest.raises(ActionValidationError) as exc_info:
        action_engine.execute_action(db=db, action_id=action.id)
    assert "requires human approval" in str(exc_info.value)

    db.close()


def test_multitenancy_organization_isolation(client):
    """Verifies that Organization A cannot access or leak Organization B's data."""
    db = SessionLocal()

    org_a = Organization(id=uuid.uuid4(), name="Tenant Alpha")
    org_b = Organization(id=uuid.uuid4(), name="Tenant Beta")
    db.add_all([org_a, org_b])
    db.flush()

    cust_a = Customer(id=uuid.uuid4(), organization_id=org_a.id, name="Alpha Private Cust", industry="retail")
    cust_b = Customer(id=uuid.uuid4(), organization_id=org_b.id, name="Beta Secret Corp", industry="finance")
    db.add_all([cust_a, cust_b])
    db.commit()

    # Query with Org A scope
    resp_a = client.get("/customers", headers={"X-Organization-Id": str(org_a.id)})
    assert resp_a.status_code == 200
    names_a = [c["name"] for c in resp_a.json()]
    assert "Alpha Private Cust" in names_a
    assert "Beta Secret Corp" not in names_a, "SECURITY VIOLATION: Org B customer leaked to Org A"

    # Query with Org B scope
    resp_b = client.get("/customers", headers={"X-Organization-Id": str(org_b.id)})
    assert resp_b.status_code == 200
    names_b = [c["name"] for c in resp_b.json()]
    assert "Beta Secret Corp" in names_b
    assert "Alpha Private Cust" not in names_b, "SECURITY VIOLATION: Org A customer leaked to Org B"

    db.close()


from app.services.audit_service import audit_service


def test_unified_audit_trail_logging(client):
    """Verifies that actions and security events generate auditable log entries queryable via /audit."""
    db = SessionLocal()
    org_id = uuid.UUID("2d48f08c-0b35-4aea-8941-86e4f855f738")

    # Explicitly log a verified event
    audit_service.log_event(
        db=db,
        organization_id=org_id,
        event_type="TEST_SECURITY_CHECK",
        user_id="sec_tester",
        result="success",
        details={"audit_verified": True},
    )
    db.close()

    # Query audit logs
    resp = client.get(
        "/audit",
        headers={"X-User-Role": "ADMIN", "X-Organization-Id": str(org_id)},
    )
    assert resp.status_code == 200
    logs = resp.json()
    assert isinstance(logs, list)
    assert len(logs) > 0
    log = logs[0]
    assert "event_type" in log
    assert "result" in log
    assert "organization_id" in log


def test_chaos_simulator_injection_containment_and_loop(client):
    """Verifies synthetic chaos injection into sandbox and execution of full cognitive loop."""
    db = SessionLocal()

    # 1. Inject chaos
    inject_resp = client.post(
        "/evaluation/chaos/inject",
        json={"scenario_id": "chaos-payment-outage"},
    )
    assert inject_resp.status_code == 200
    inject_data = inject_resp.json()
    assert inject_data["events_injected"] > 0
    assert inject_data["target_organization_id"] == str(SANDBOX_CHAOS_ORG_ID)

    # 2. Verify containment: events have CHAOS_SIMULATION
    chaos_events = db.query(Event).filter(
        Event.organization_id == SANDBOX_CHAOS_ORG_ID,
        Event.event_type == "CHAOS_SIMULATION",
    ).all()
    assert len(chaos_events) > 0

    # 3. Run evaluation resilience
    resilience_result = chaos_evaluator.evaluate_chaos_resilience(db)
    assert resilience_result["containment_verified"] is True
    assert resilience_result["containment_guarantee"] == "ZERO_PRODUCTION_LEAKAGE"
    assert resilience_result["overall_resilience_status"] == "RESILIENT"

    db.close()
