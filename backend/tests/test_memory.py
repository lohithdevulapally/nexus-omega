"""Test Hindsight Memory Service."""

from unittest.mock import MagicMock
import pytest
from app.services.memory_service import MemoryService


@pytest.fixture
def mock_memory_service():
    service = MemoryService(base_url="http://localhost:8888")
    service.client = MagicMock()
    return service


def test_create_memory_bank_mock(mock_memory_service):
    mock_memory_service.client.create_bank.return_value = {"status": "created"}
    res = mock_memory_service.create_memory_bank(bank_id="test-bank", name="Test Bank")
    assert res is True
    mock_memory_service.client.create_bank.assert_called_once()


def test_retain_experience_mock(mock_memory_service):
    mock_memory_service.client.retain.return_value = MagicMock(operation_id="op-123")
    res = mock_memory_service.retain_experience(
        content="ACME experienced payment failures",
        bank_id="test-bank",
    )
    assert res["success"] is True
    assert res["bank_id"] == "test-bank"


def test_recall_memories_mock(mock_memory_service):
    mock_result_item = MagicMock(
        id="mem-1",
        text="Gateway retry worked twice",
        type="experience",
        entities=None,
        context=None,
        metadata={"experience_id": "123"},
        tags=["incident"],
        scores=None,
    )
    mock_response = MagicMock(results=[mock_result_item])
    mock_memory_service.client.recall.return_value = mock_response

    memories = mock_memory_service.recall_memories(
        query="payment failures",
        bank_id="test-bank",
    )
    assert len(memories) == 1
    assert memories[0]["text"] == "Gateway retry worked twice"


def test_reflect_on_memories_mock(mock_memory_service):
    mock_response = MagicMock(
        text="Historical pattern shows gateway switching succeeds after 2 retry attempts.",
        based_on=["mem-1"],
        structured_output=None,
    )
    mock_memory_service.client.reflect.return_value = mock_response

    reflection = mock_memory_service.reflect_on_memories(
        query="What have we learned from ACME payment failures?",
        bank_id="test-bank",
    )
    assert "Historical pattern" in reflection["text"]
    assert reflection["bank_id"] == "test-bank"
