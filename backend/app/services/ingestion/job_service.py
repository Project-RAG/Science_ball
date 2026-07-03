from __future__ import annotations

import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.ingestion_jobs import IngestionJobRepository
from app.schemas.ingestion import IngestionJobResponse
from app.worker.tasks import process_document_ingestion

class IngestionJobService:
    """Orchestrates the ingestion job lifecycle."""

    def __init__(self, repository: IngestionJobRepository):
        self.repository = repository

    async def create_and_enqueue_job(
        self,
        session: AsyncSession,
        document_id: uuid.UUID,
        created_by: uuid.UUID | None = None
    ) -> IngestionJobResponse:
        """Create a DB record and trigger the Celery task."""
        # 1. Create job in DB as 'pending'
        job = await self.repository.create(session, document_id, created_by)

        # 2. Trigger async Celery task
        process_document_ingestion.delay(str(job.id))

        return IngestionJobResponse.model_validate(job)

    async def get_job_status(self, session: AsyncSession, job_id: uuid.UUID) -> IngestionJobResponse | None:
        """Fetch the current status of a job."""
        job = await self.repository.get_by_id(session, job_id)
        if not job:
            return None
        return IngestionJobResponse.model_validate(job)

    async def retry_job(self, session: AsyncSession, job_id: uuid.UUID) -> IngestionJobResponse:
        """Reset a failed/stopped job and re-enqueue it."""
        # Reset status to pending
        await self.repository.update_status(
            session=session,
            job_id=job_id,
            status="pending",
            progress=0.0,
            error_message=None
        )

        # Trigger task again
        process_document_ingestion.delay(str(job_id))

        # Return updated state
        job = await self.repository.get_by_id(session, job_id)
        return IngestionJobResponse.model_validate(job)
