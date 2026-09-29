"""Test Chat endpoint and conversational memory integration."""

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

# Test DB setup with StaticPool so all sessions share the in-memory database
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
def setup_test_data():
    app.dependency_overrides[get_db] = override_get_db
    db = TestingSessionLocal()
    # Clear and setup
    db.query(Experience).delete()
    db.query(Customer).delete()
    db.query(Organization).delete()
    db.commit()

    org = Organization(name="Test Chat Org")
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

    exp = Experience(
        organization_id=org.id,
        experience_type="incident_resolution",
        description="ACME Corp payment failures were resolved by switching gateways.",
        action_taken="Switched gateway",
        outcome="Payment success rate recovered",
        success=True,
        hindsight_bank_id="nexus-demo",
    )
    db.add(exp)
    db.commit()

    yield org

    db.close()
    app.dependency_overrides.pop(get_db, None)


def test_chat_acme_history_query(setup_test_data):
    org = setup_test_data
    payload = {
        "organization_id": str(org.id),
        "message": "ACME previously had payment failures. What happened?",
    }

    with patch("app.services.memory_service.memory_service.recall_memories") as mock_recall:
        mock_recall.return_value = [
            {"id": "1", "text": "Customer ACME Corp experienced three payment failures. First two resolved by retry, third by gateway switch."}
        ]
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["memory_used"] is True
        assert "ACME Corp" in data["message"]
        assert len(data["memories"]) > 0


def test_chat_recommendation_avoid_mistakes(setup_test_data):
    org = setup_test_data
    payload = {
        "organization_id": str(org.id),
        "message": "What should we avoid doing if ACME has the same problem again?",
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "avoid" in data["message"].lower() or "generic" in data["message"].lower()


def test_chat_experience_ingestion(setup_test_data):
    org = setup_test_data
    payload = {
        "organization_id": str(org.id),
        "message": "We switched ACME to Gateway B and payment failures stopped.",
    }

    with patch("app.services.memory_service.memory_service.retain_experience") as mock_retain:
        mock_retain.return_value = {"success": True}
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "EXPERIENCE"
        assert data["experience_stored"] is True
