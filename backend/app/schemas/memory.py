"""Memory Schemas for Hindsight Retention, Recall, and Reflection."""

import uuid
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class MemoryRetainRequest(BaseModel):
    organization_id: uuid.UUID = Field(
        ...,
        description="Organization ID owning this memory",
        json_schema_extra={"example": "11111111-1111-1111-1111-111111111111"},
    )
    content: str = Field(
        ...,
        description="The narrative experience or observation to retain",
        json_schema_extra={"example": "Customer ACME Corp experienced three payment failures during September 2026."},
    )
    experience_type: str = Field(
        "incident_resolution",
        description="Category of experience",
        json_schema_extra={"example": "incident_resolution"},
    )
    context: Optional[str] = Field(None, description="Additional context or background information")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadata tags and attributes")


class MemoryRetainResponse(BaseModel):
    success: bool
    bank_id: str
    experience_id: Optional[uuid.UUID] = None
    operation_id: Optional[str] = None
    message: str


class MemorySearchResponse(BaseModel):
    bank_id: str
    query: str
    count: int
    memories: List[Dict[str, Any]]


class MemoryReflectRequest(BaseModel):
    organization_id: uuid.UUID = Field(..., description="Organization ID to reflect across")
    query: str = Field(
        ...,
        description="Strategic question to synthesize and reflect upon",
        json_schema_extra={"example": "What have we learned from ACME's previous payment failures?"},
    )
    context: Optional[str] = Field(None, description="Contextual constraints or notes")


class MemoryReflectResponse(BaseModel):
    bank_id: str
    query: str
    reflection: str
    based_on: Optional[List[Any]] = Field(default_factory=list)
