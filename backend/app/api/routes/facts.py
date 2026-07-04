from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.postgres import get_db
from app.schemas.facts import (
    FactDetailResponse,
    FactReviewRequest,
    FactRejectRequest,
    FactEditRequest
)
from app.services.review.fact_review_service import FactReviewService
from app.repositories.facts import FactsRepository
from app.repositories.audit_logs import AuditLogRepository

router = APIRouter(prefix="/facts", tags=["Verification"])

# Dependency for the review service
async def get_fact_review_service(session: AsyncSession = Depends(get_db)) -> FactReviewService:
    return FactReviewService(FactsRepository(), AuditLogRepository())

@router.get("/pending-review", response_model=List[FactDetailResponse])
async def list_pending_facts(
    document_id: UUID | None = None,
    min_confidence: float | None = None,
    max_confidence: float | None = None,
    session: AsyncSession = Depends(get_db),
    service: FactReviewService = Depends(get_fact_review_service)
):
    """List facts awaiting human verification."""
    facts = await service.list_pending_facts(
        session, document_id, min_confidence, max_confidence
    )
    return facts

@router.post("/{fact_id}/verify", status_code=status.HTTP_204_NO_CONTENT)
async def verify_fact(
    fact_id: UUID,
    request: FactReviewRequest,
    session: AsyncSession = Depends(get_db),
    service: FactReviewService = Depends(get_fact_review_service),
    user_id: UUID | None = None # Placeholder for actual JWT auth
):
    """Mark a fact as verified."""
    try:
        await service.verify_fact(session, fact_id, user_id, request.comment)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None

@router.post("/{fact_id}/reject", status_code=status.HTTP_204_NO_CONTENT)
async def reject_fact(
    fact_id: UUID,
    request: FactRejectRequest,
    session: AsyncSession = Depends(get_db),
    service: FactReviewService = Depends(get_fact_review_service),
    user_id: UUID | None = None # Placeholder for actual JWT auth
):
    """Mark a fact as rejected."""
    try:
        await service.reject_fact(session, fact_id, user_id, request.reason)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None

@router.post("/{fact_id}/comment", status_code=status.HTTP_204_NO_CONTENT)
async def add_fact_comment(
    fact_id: UUID,
    request: FactReviewRequest,
    session: AsyncSession = Depends(get_db),
    service: FactReviewService = Depends(get_fact_review_service),
    user_id: UUID | None = None # Placeholder for actual JWT auth
):
    """Add a review comment to the audit log."""
    try:
        await service.add_review_comment(session, fact_id, user_id, request.comment or "")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None

@router.patch("/{fact_id}", response_model=FactDetailResponse)
async def edit_fact(
    fact_id: UUID,
    request: FactEditRequest,
    session: AsyncSession = Depends(get_db),
    service: FactReviewService = Depends(get_fact_review_service),
    user_id: UUID | None = None # Placeholder for actual JWT auth
):
    """Edit a fact and mark it as verified."""
    try:
        # Convert request to dict excluding None values
        updates = {k: v for k, v in request.dict().items() if v is not None}
        # Remove 'comment' from updates as it's used for the audit log
        comment = updates.pop("comment", None)

        await service.edit_and_verify_fact(session, fact_id, user_id, updates, comment)

        # Return updated fact
        from sqlalchemy import select
        from app.models.fact import Fact
        stmt = select(Fact).where(Fact.id == fact_id)
        result = await session.execute(stmt)
        return result.scalar_one()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
