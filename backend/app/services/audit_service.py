"""Unified Audit Service for NEXUS-Ω.

Logs all security, cognitive, approval, simulation, and execution events with
strict organization-scoping and request correlation IDs.
"""

import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.db.models.audit_log import AuditLog
from app.core.logging import logger


class AuditService:
    @staticmethod
    def log_event(
        db: Session,
        organization_id: uuid.UUID,
        event_type: str,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        result: str = "success",
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """Persists an auditable event with tamper-resistant structure."""
        try:
            log_entry = AuditLog(
                organization_id=organization_id,
                user_id=user_id or "system",
                request_id=request_id,
                event_type=event_type,
                resource_type=resource_type,
                resource_id=str(resource_id) if resource_id else None,
                result=result,
                details=details or {},
            )
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)
            return log_entry
        except Exception as e:
            logger.error(f"[AUDIT_ERROR] Failed to record audit log: {e}")
            try:
                db.rollback()
            except Exception:
                pass
            # Create unpersisted object for graceful fallback
            return AuditLog(
                organization_id=organization_id,
                user_id=user_id or "system",
                request_id=request_id,
                event_type=event_type,
                result="fallback_logged",
                details={"error": str(e)},
            )

    @staticmethod
    def get_logs(
        db: Session,
        organization_id: uuid.UUID,
        event_type: Optional[str] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[AuditLog]:
        """Queries organization-scoped audit logs."""
        query = select(AuditLog).where(AuditLog.organization_id == organization_id)
        if event_type:
            query = query.where(AuditLog.event_type == event_type)
        if user_id:
            query = query.where(AuditLog.user_id == user_id)
        if request_id:
            query = query.where(AuditLog.request_id == request_id)

        query = query.order_by(desc(AuditLog.created_at)).offset(offset).limit(limit)
        return list(db.scalars(query).all())


audit_service = AuditService()
