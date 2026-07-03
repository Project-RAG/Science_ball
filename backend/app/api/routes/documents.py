"""Document upload endpoint.

Thin route — delegates all business logic to the upload service.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, get_minio_client
from app.schemas.documents import DocumentResponse
from app.services.ingestion.document_upload_service import upload_document

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentResponse, status_code=201)
async def upload(
    file: UploadFile = File(...),
    title: str = Form(...),
    source_type: str = Form(...),
    access_level: str = Form(...),
    language: str | None = Form(None),
    year: int | None = Form(None),
    session: AsyncSession = Depends(get_db_session),
    minio_client = Depends(get_minio_client),
) -> DocumentResponse:
    """Upload a document file to MinIO and persist its metadata.

    Allowed file types: .pdf, .docx, .txt, .md, .csv, .xlsx
    """
    file_bytes = await file.read()
    content_type = file.content_type or "application/octet-stream"

    result = await upload_document(
        session=session,
        minio_client=minio_client,
        file_bytes=file_bytes,
        filename=file.filename or "unnamed",
        content_type=content_type,
        title=title,
        source_type=source_type,
        access_level=access_level,
        language=language,
        year=year,
    )

    await session.commit()
    return result
