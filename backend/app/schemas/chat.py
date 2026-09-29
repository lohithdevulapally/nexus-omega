"""Chat Schemas."""

import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    organization_id: uuid.UUID = Field(
        ...,
        description="Organization identifier",
        json_schema_extra={"example": "11111111-1111-1111-1111-111111111111"},
    )
    message: str = Field(
        ...,
        description="User prompt or message",
        json_schema_extra={"example": "ACME previously had payment failures. What happened?"},
    )
    conversation_id: Optional[str] = Field(None, description="Optional conversation session ID")


class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    memory_used: bool
    classification: str
    memories: List[Dict[str, Any]] = Field(default_factory=list)
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    experience_stored: bool = False
