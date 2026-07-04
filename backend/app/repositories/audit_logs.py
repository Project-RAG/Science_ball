"""Repository for persisting immutable audit logs."""

from __future__ import annotations

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from app.models.audit_log import AuditLog

class AuditLogRepository:
    """
    Handles persistence of system audit logs.
    Audit logs are immutable; only creation is supported.
    """

    async def create(
        self,
        session: AsyncSession,
        user_id: uuid.UUID | None,
        action: str,
        entity_type: str | None = None,
        entity_id: str | None = None,
        payload: dict | None = None
    ) -> AuditLog:
        """
        Creates a new audit log entry.
        """
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload
        )
        session.add(log_entry)
        await session.flush()
        return log_entry
