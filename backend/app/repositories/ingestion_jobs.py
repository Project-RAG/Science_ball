from __future__ import annotations

import uuid
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ingestion_job import IngestionJob


class IngestionJobRepository:
    """Repository for managing ingestion job state in PostgreSQL."""

    async def create(self, session: AsyncSession, document_id: uuid.UUID, created_by: uuid.UUID | None = None) -> IngestionJob:
        """Create a new ingestion job with status 'pending'."""
        job = IngestionJob(
            document_id=document_id,
            created_by=created_by,
            status="pending",
            progress=0.0
        )
        session.add(job)
        await session.flush()
        return job

    async def get_by_id(self, session: AsyncSession, job_id: uuid.UUID) -> IngestionJob | None:
        """Fetch a single ingestion job by its ID."""
        result = await session.execute(select(IngestionJob).where(IngestionJob.id == job_id))
        return result.scalar_one_or_none()

    async def update_status(
        self,
        session: AsyncSession,
        job_id: uuid.UUID,
        status: str,
        progress: float | None = None,
        error_message: str | None = None
    ) -> None:
        """Update the status and progress of an existing job."""
        await session.execute(
            update(IngestionJob)
            .where(IngestionJob.id == job_id)
            .values(status=status, progress=progress, error_message=error_message)
        )

    async def get_by_document_id(self, session: AsyncSession, document_id: uuid.UUID) -> IngestionJob | None:
        """Get the latest job for a specific document."""
        result = await session.execute(
            select(IngestionJob)
            .where(IngestionJob.document_id == document_id)
            .order_by(IngestionJob.created_at.desc())
        )
        return result.scalar_one_or_none()
