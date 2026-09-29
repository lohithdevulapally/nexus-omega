"""Audit Log API Router for NEXUS-Ω."""

import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.database import get_db
from app.services.audit_service import audit_service
from app.core.security import require_permission, Permission, AuthContext

router = APIRouter(prefix="/audit", tags=["Audit Trail"])


class AuditLogResponse(BaseModel):
    id: str
    organization_id: str
    user_id: Optional[str]
    request_id: Optional[str]
    event_type: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    result: str
    details: dict
    created_at: str


@router.get("", response_model=List[AuditLogResponse], summary="Query Audit Logs")
def get_audit_trail(
    event_type: Optional[str] = None,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission(Permission.VIEW)),
):
    """Retrieves organization-scoped tamper-evident audit logs."""
    logs = audit_service.get_logs(
        db=db,
        organization_id=auth.organization_id,
        event_type=event_type,
        user_id=user_id,
        request_id=request_id,
        limit=limit,
        offset=offset,
    )
    return [
        AuditLogResponse(
            id=str(log.id),
            organization_id=str(log.organization_id),
            user_id=log.user_id,
            request_id=log.request_id,
            event_type=log.event_type,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            result=log.result,
            details=log.details or {},
            created_at=log.created_at.isoformat() if log.created_at else "",
        )
        for log in logs
    ]
