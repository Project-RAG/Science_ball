"""Pydantic schemas for document upload."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

MVP_ALLOWED_EXTENSIONS: set[str] = {".pdf", ".docx", ".txt", ".md", ".csv", ".xlsx"}


class DocumentResponse(BaseModel):
    """Public document metadata returned after upload."""

    id: UUID
    title: str
    source_type: str
    access_level: str
    language: str | None = None
    year: int | None = None
    minio_bucket: str
    minio_object_key: str
    checksum: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
