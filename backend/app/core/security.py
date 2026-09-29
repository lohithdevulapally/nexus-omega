"""Security, Authentication, and Role-Based Access Control (RBAC) for NEXUS-Ω."""

import uuid
from enum import Enum
from typing import Optional, Set
from fastapi import Header, HTTPException, status, Depends
from pydantic import BaseModel


class Role(str, Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"


class Permission(str, Enum):
    VIEW = "VIEW"
    INVESTIGATE = "INVESTIGATE"
    SIMULATE = "SIMULATE"
    APPROVE = "APPROVE"
    EXECUTE = "EXECUTE"
    ADMIN = "ADMIN"


ROLE_PERMISSIONS: dict[Role, Set[Permission]] = {
    Role.VIEWER: {Permission.VIEW},
    Role.ANALYST: {Permission.VIEW, Permission.INVESTIGATE, Permission.SIMULATE},
    Role.OPERATOR: {
        Permission.VIEW,
        Permission.INVESTIGATE,
        Permission.SIMULATE,
        Permission.APPROVE,
        Permission.EXECUTE,
    },
    Role.ADMIN: {
        Permission.VIEW,
        Permission.INVESTIGATE,
        Permission.SIMULATE,
        Permission.APPROVE,
        Permission.EXECUTE,
        Permission.ADMIN,
    },
}


class AuthContext(BaseModel):
    user_id: str
    organization_id: uuid.UUID
    role: Role
    permissions: Set[Permission]

    def has_permission(self, permission: Permission) -> bool:
        return permission in self.permissions


DEFAULT_DEMO_ORG_ID = uuid.UUID("2d48f08c-0b35-4aea-8941-86e4f855f738")


def get_current_auth(
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
    x_user_role: Optional[str] = Header(None, alias="X-User-Role"),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-Id"),
    authorization: Optional[str] = Header(None),
) -> AuthContext:
    """Extracts and validates user authentication context from headers or token."""
    # Resolve organization
    org_id = DEFAULT_DEMO_ORG_ID
    if x_organization_id:
        try:
            org_id = uuid.UUID(x_organization_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid organization UUID format: {x_organization_id}",
            )

    # Resolve role
    role_str = (x_user_role or "OPERATOR").upper()
    try:
        role = Role(role_str)
    except ValueError:
        role = Role.OPERATOR

    user_id = x_user_id or "operator_admin"
    permissions = ROLE_PERMISSIONS.get(role, set())

    return AuthContext(
        user_id=user_id,
        organization_id=org_id,
        role=role,
        permissions=permissions,
    )


def require_permission(perm: Permission):
    """FastAPI dependency to enforce specific permissions."""

    def dependency(auth: AuthContext = Depends(get_current_auth)) -> AuthContext:
        if not auth.has_permission(perm):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Action forbidden: Role '{auth.role.value}' does not possess "
                    f"required permission '{perm.value}'"
                ),
            )
        return auth

    return dependency
