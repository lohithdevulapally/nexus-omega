"""Test database models and relationships."""

import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.models import (
    Organization,
    Customer,
    Event,
    Experience,
    Decision,
    Action,
    AgentRun,
    MemoryReference,
)


@pytest.fixture
def db_session():
    # Use SQLite in-memory for fast, hermetic unit tests
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_organization_and_customer_creation(db_session):
    org = Organization(name="Test Org")
    db_session.add(org)
    db_session.commit()
    assert org.id is not None

    cust = Customer(
        organization_id=org.id,
        name="ACME Corp",
        industry="E-commerce",
        status="active",
        risk_level="high",
        metadata_json={"plan": "enterprise"},
    )
    db_session.add(cust)
    db_session.commit()
    assert cust.id is not None
    assert cust.organization_id == org.id


def test_experience_and_memory_reference(db_session):
    org = Organization(name="Memory Org")
    db_session.add(org)
    db_session.commit()

    ev = Event(
        organization_id=org.id,
        event_type="incident",
        title="Gateway Timeout",
        description="Gateway timed out on primary rail",
    )
    db_session.add(ev)
    db_session.commit()

    exp = Experience(
        organization_id=org.id,
        event_id=ev.id,
        experience_type="incident_resolution",
        description="Gateway failure resolved by retry",
        action_taken="Gateway retry",
        outcome="Resolved successfully",
        success=True,
        hindsight_bank_id="test-bank",
    )
    db_session.add(exp)
    db_session.commit()
    assert exp.id is not None

    mem_ref = MemoryReference(
        organization_id=org.id,
        entity_type="experience",
        entity_id=str(exp.id),
        hindsight_bank_id="test-bank",
        memory_context=exp.description,
    )
    db_session.add(mem_ref)
    db_session.commit()
    assert mem_ref.id is not None


def test_decision_and_action(db_session):
    org = Organization(name="Decision Org")
    db_session.add(org)
    db_session.commit()

    dec = Decision(
        organization_id=org.id,
        title="Gateway Multi-Rail Migration",
        problem="Single gateway failure",
        decision="Deploy backup gateway",
        status="approved",
    )
    db_session.add(dec)
    db_session.commit()
    assert dec.id is not None

    action = Action(
        organization_id=org.id,
        decision_id=dec.id,
        action_type="deploy_proxy",
        payload={"target": "gateway-proxy"},
        status="completed",
    )
    db_session.add(action)
    db_session.commit()
    assert action.id is not None
    assert action.decision_id == dec.id
