from __future__ import annotations

from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional
from datetime import datetime

class FactDetailResponse(BaseModel):
    id: UUID
    subject_id: str
    subject_type: str
    predicate: str
    object_id: str
    object_type: str
    confidence: float
    verification_status: str
    source_document_id: UUID
    source_chunk_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

class FactReviewRequest(BaseModel):
    comment: Optional[str] = Field(None, description="Reviewer's comment or reason for decision")

class FactRejectRequest(BaseModel):
    reason: str = Field(..., min_length=1, description="Reason why the fact is rejected")

class FactEditRequest(BaseModel):
    subject_id: Optional[str] = None
    subject_type: Optional[str] = None
    predicate: Optional[str] = None
    object_id: Optional[str] = None
    object_type: Optional[str] = None
    confidence: Optional[float] = None
    comment: Optional[str] = Field(None, description="Reason for editing the fact")

class FactVersionResponse(BaseModel):
    version: int
    payload: dict
    changed_by: Optional[UUID] = None
    change_reason: Optional[str] = None
    created_at: datetime
