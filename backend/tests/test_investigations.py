"""Test Investigation endpoints: 'Have We Seen This Before?' and 'Don't Repeat Our Mistake'."""

import uuid
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.database import get_db
from app.db.models import Organization, Customer, Experience

client = TestClient(app)

from sqlalchemy.pool import StaticPool

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
Base.metadata.create_all(bind=test_engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_investigation_data():
    app.dependency_overrides[get_db] = override_get_db
    db = TestingSessionLocal()
    db.query(Experience).delete()
    db.query(Customer).delete()
    db.query(Organization).delete()
    db.commit()

    org = Organization(name="Investigation Org")
    db.add(org)
    db.commit()
    db.refresh(org)

    cust = Customer(
        organization_id=org.id,
        name="ACME Corp",
        industry="E-commerce",
        status="active",
        risk_level="high",
    )
    db.add(cust)

    # Failed restart experience
    exp_failed = Experience(
        organization_id=org.id,
        experience_type="operational_mistake",
        description="Payment service restarted under connection pool leak.",
        action_taken="Restart the payment service",
        outcome="Restart did not clear connection starvation; failure returned after 20 minutes.",
        success=False,
        hindsight_bank_id="nexus-demo",
    )
    db.add(exp_failed)

    # Successful gateway switch experience
    exp_success = Experience(
        organization_id=org.id,
        experience_type="incident_resolution",
        description="ACME recurring payment timeout.",
        action_taken="Switched gateway to secondary provider",
        outcome="Payment processing resumed immediately.",
        success=True,
        hindsight_bank_id="nexus-demo",
    )
    db.add(exp_success)
    db.commit()

    yield org

    db.close()
    app.dependency_overrides.pop(get_db, None)


def test_have_we_seen_this_before(setup_investigation_data):
    org = setup_investigation_data
    payload = {
        "organization_id": str(org.id),
        "description": "ACME is experiencing payment failures again.",
    }

    with patch("app.services.memory_service.memory_service.recall_memories") as mock_recall:
        mock_recall.return_value = [
            {"id": "m1", "text": "Customer ACME Corp experienced payment failure incident previously."}
        ]
        response = client.post("/investigations/similar", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["similarity_found"] is True
        assert len(data["historical_cases"]) > 0
        assert "Historical pattern detected" in data["analysis_summary"]


def test_dont_repeat_our_mistake_warning(setup_investigation_data):
    org = setup_investigation_data
    payload = {
        "organization_id": str(org.id),
        "proposed_action": "Restart the payment service.",
    }

    response = client.post("/investigations/avoid-mistakes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["warning"] is True
    assert "did not resolve" in data["reason"] or "Restart" in data["reason"]
    assert len(data["historical_cases"]) > 0
    assert len(data["alternative_successful_actions"]) > 0
