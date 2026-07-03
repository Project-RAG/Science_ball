from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, get_ingestion_service
from app.repositories.ingestion_jobs import IngestionJobRepository
from app.schemas.ingestion import IngestionJobResponse, RetryRequest
from app.services.ingestion.job_service import IngestionJobService

router = APIRouter(prefix="/ingestion/jobs", tags=["ingestion"])


@router.get("/{job_id}", response_model=IngestionJobResponse)
async def get_job_status(
    job_id: uuid.UUID = Path(...),
    session: AsyncSession = Depends(get_db_session),
    job_service: IngestionJobService = Depends(get_ingestion_service),
) -> IngestionJobResponse:
    """Get the current status and progress of an ingestion job."""
    job = await job_service.get_job_status(session, job_id)
    if not job:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Ingestion job not found")
    return job


@router.post("/{job_id}/retry", response_model=IngestionJobResponse)
async def retry_job(
    job_id: uuid.UUID = Path(...),
    request: RetryRequest = Depends(),
    session: AsyncSession = Depends(get_db_session),
    job_service: IngestionJobService = Depends(get_ingestion_service),
) -> IngestionJobResponse:
    """Trigger a retry for a failed or stopped ingestion job."""
    return await job_service.retry_job(session, job_id)
