"""Tests for document upload service.

All tests use mocks/fakes for MinIO and PostgreSQL — no live services required.
"""

from __future__ import annotations

import hashlib
import io
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


# ── Helpers ─────────────────────────────────────────────────────────────


def _make_fake_session() -> AsyncMock:
    """Return an AsyncMock that behaves like an AsyncSession.

    The mock simulates DB-side timestamp defaults by setting
    created_at / updated_at on any object passed to session.add().
    """
    from datetime import datetime, timezone

    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.flush = AsyncMock()

    def _add(obj: object) -> None:
        now = datetime.now(timezone.utc)
        if hasattr(obj, "created_at"):
            obj.created_at = now
        if hasattr(obj, "updated_at"):
            obj.updated_at = now

    session.add = MagicMock(side_effect=_add)
    return session


def _make_fake_minio() -> MagicMock:
    """Return a MagicMock that behaves like a Minio client."""
    client = MagicMock()
    client.bucket_exists.return_value = True
    client.put_object.return_value = None
    client.make_bucket.return_value = None
    return client


# ── Extension validation ────────────────────────────────────────────────


class TestExtensionValidation:
    def test_allowed_extensions_pass(self):
        from app.services.ingestion.document_upload_service import _validate_extension

        for ext in [".pdf", ".docx", ".txt", ".md", ".csv", ".xlsx"]:
            assert _validate_extension(f"doc{ext}") == ext

    def test_uppercase_extension_is_normalized(self):
        from app.services.ingestion.document_upload_service import _validate_extension

        assert _validate_extension("REPORT.PDF") == ".pdf"

    def test_unknown_extension_raises_value_error(self):
        from app.services.ingestion.document_upload_service import _validate_extension

        with pytest.raises(ValueError, match="Unsupported file type"):
            _validate_extension("image.png")

    def test_no_extension_raises_value_error(self):
        from app.services.ingestion.document_upload_service import _validate_extension

        with pytest.raises(ValueError, match="Unsupported file type"):
            _validate_extension("noextension")


# ── Checksum ────────────────────────────────────────────────────────────


class TestChecksum:
    def test_checksum_is_sha256_hex(self):
        from app.services.ingestion.document_upload_service import _calculate_checksum

        data = b"hello world"
        expected = hashlib.sha256(data).hexdigest()
        assert _calculate_checksum(data) == expected

    def test_checksum_is_deterministic(self):
        from app.services.ingestion.document_upload_service import _calculate_checksum

        data = b"test content"
        assert _calculate_checksum(data) == _calculate_checksum(data)

    def test_different_content_different_checksum(self):
        from app.services.ingestion.document_upload_service import _calculate_checksum

        assert _calculate_checksum(b"a") != _calculate_checksum(b"b")


# ── Object key ──────────────────────────────────────────────────────────


class TestObjectKey:
    def test_object_key_contains_document_id_and_extension(self):
        from app.services.ingestion.document_upload_service import _build_object_key

        doc_id = uuid.uuid4()
        key = _build_object_key(doc_id, ".pdf")
        assert str(doc_id) in key
        assert key.endswith(".pdf")
        assert key.startswith("documents/")


# ── Upload service (mocked MinIO + DB) ──────────────────────────────────


class TestUploadDocumentService:
    @pytest.fixture
    def anyio_backend(self) -> str:
        return "asyncio"

    @pytest.mark.anyio
    async def test_upload_document_returns_response(self):
        from app.services.ingestion.document_upload_service import upload_document

        session = _make_fake_session()
        minio_client = _make_fake_minio()

        result = await upload_document(
            session=session,
            minio_client=minio_client,
            file_bytes=b"fake pdf content",
            filename="report.pdf",
            content_type="application/pdf",
            title="Test Report",
            source_type="publication",
            access_level="internal",
            language="en",
            year=2025,
        )

        assert result.title == "Test Report"
        assert result.source_type == "publication"
        assert result.access_level == "internal"
        assert result.language == "en"
        assert result.year == 2025
        assert result.minio_bucket is not None
        assert result.minio_object_key is not None
        assert result.checksum is not None
        assert isinstance(result.id, uuid.UUID)

    @pytest.mark.anyio
    async def test_upload_document_stores_file_in_minio(self):
        from app.services.ingestion.document_upload_service import upload_document

        session = _make_fake_session()
        minio_client = _make_fake_minio()

        await upload_document(
            session=session,
            minio_client=minio_client,
            file_bytes=b"content",
            filename="notes.txt",
            content_type="text/plain",
            title="Notes",
            source_type="report",
            access_level="public",
        )

        minio_client.put_object.assert_called_once()
        call_kwargs = minio_client.put_object.call_args.kwargs
        assert call_kwargs["bucket_name"] is not None
        assert call_kwargs["object_name"] is not None
        assert call_kwargs["length"] == len(b"content")

    @pytest.mark.anyio
    async def test_upload_document_creates_bucket_if_missing(self):
        from app.services.ingestion.document_upload_service import upload_document

        session = _make_fake_session()
        minio_client = _make_fake_minio()
        minio_client.bucket_exists.return_value = False

        await upload_document(
            session=session,
            minio_client=minio_client,
            file_bytes=b"data",
            filename="doc.md",
            content_type="text/markdown",
            title="Doc",
            source_type="publication",
            access_level="internal",
        )

        minio_client.make_bucket.assert_called_once()

    @pytest.mark.anyio
    async def test_upload_document_persists_metadata_in_db(self):
        from app.services.ingestion.document_upload_service import upload_document

        session = _make_fake_session()
        minio_client = _make_fake_minio()

        await upload_document(
            session=session,
            minio_client=minio_client,
            file_bytes=b"csv data",
            filename="data.csv",
            content_type="text/csv",
            title="Dataset",
            source_type="report",
            access_level="internal",
        )

        # session.add() must have been called with a Document instance.
        session.add.assert_called_once()
        session.flush.assert_called_once()

    @pytest.mark.anyio
    async def test_upload_document_rejects_unknown_extension(self):
        from app.services.ingestion.document_upload_service import upload_document

        session = _make_fake_session()
        minio_client = _make_fake_minio()

        with pytest.raises(ValueError, match="Unsupported file type"):
            await upload_document(
                session=session,
                minio_client=minio_client,
                file_bytes=b"image",
                filename="photo.png",
                content_type="image/png",
                title="Photo",
                source_type="publication",
                access_level="internal",
            )

        # MinIO and DB must not be touched on validation failure.
        minio_client.put_object.assert_not_called()
        session.add.assert_not_called()


# ── API endpoint (mocked dependencies) ──────────────────────────────────


class TestDocumentsApi:
    @pytest.fixture
    def anyio_backend(self) -> str:
        return "asyncio"

    @pytest.mark.anyio
    async def test_upload_endpoint_returns_201(self):
        from unittest.mock import AsyncMock, patch

        from httpx import ASGITransport, AsyncClient

        from app.main import app

        # Build a fake document to return from the mocked service.
        fake_doc_id = uuid.uuid4()
        fake_response = {
            "id": str(fake_doc_id),
            "title": "Test",
            "source_type": "publication",
            "access_level": "internal",
            "language": None,
            "year": None,
            "minio_bucket": "rd-documents",
            "minio_object_key": f"documents/{fake_doc_id}/{fake_doc_id}.pdf",
            "checksum": "abc123",
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
        }

        with patch(
            "app.api.routes.documents.upload_document",
            new_callable=AsyncMock,
        ) as mock_upload:
            mock_upload.return_value = type(
                "FakeResponse",
                (),
                {
                    "model_dump": lambda self, **kw: fake_response,
                    "id": fake_doc_id,
                    "title": "Test",
                    "source_type": "publication",
                    "access_level": "internal",
                    "language": None,
                    "year": None,
                    "minio_bucket": "rd-documents",
                    "minio_object_key": f"documents/{fake_doc_id}/{fake_doc_id}.pdf",
                    "checksum": "abc123",
                    "created_at": "2025-01-01T00:00:00Z",
                    "updated_at": "2025-01-01T00:00:00Z",
                },
            )()

            # Also mock the DB session dependency.
            with patch(
                "app.dependencies.get_session_factory",
                return_value=MagicMock(
                    return_value=AsyncMock(
                        __aenter__=AsyncMock(
                            return_value=AsyncMock(
                                commit=AsyncMock(),
                                close=AsyncMock(),
                            )
                        ),
                        __aexit__=AsyncMock(return_value=None),
                    )
                ),
            ):
                with patch(
                    "app.dependencies.get_minio",
                    return_value=MagicMock(),
                ):
                    transport = ASGITransport(app=app)
                    async with AsyncClient(
                        transport=transport, base_url="http://test"
                    ) as client:
                        response = await client.post(
                            "/api/v1/documents/upload",
                            files={"file": ("test.pdf", b"pdf", "application/pdf")},
                            data={
                                "title": "Test",
                                "source_type": "publication",
                                "access_level": "internal",
                            },
                        )

            assert response.status_code == 201
            data = response.json()
            assert data["title"] == "Test"
            assert data["access_level"] == "internal"

    @pytest.mark.anyio
    async def test_upload_endpoint_rejects_missing_file(self):
        from httpx import ASGITransport, AsyncClient

        from app.main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/documents/upload",
                data={
                    "title": "Test",
                    "source_type": "publication",
                    "access_level": "internal",
                },
            )

        assert response.status_code == 422  # FastAPI validation error


# ── Repository (mocked session) ─────────────────────────────────────────


class TestDocumentRepository:
    @pytest.fixture
    def anyio_backend(self) -> str:
        return "asyncio"

    @pytest.mark.anyio
    async def test_create_document_adds_and_flushes(self):
        from app.repositories.documents import create_document

        session = _make_fake_session()

        doc = await create_document(
            session,
            title="Repo Test",
            source_type="publication",
            access_level="internal",
            minio_bucket="rd-documents",
            minio_object_key="documents/uuid/doc.pdf",
            checksum="abc",
        )

        session.add.assert_called_once()
        session.flush.assert_called_once()
        assert doc.title == "Repo Test"
        assert doc.access_level == "internal"

    @pytest.mark.anyio
    async def test_create_document_accepts_explicit_id(self):
        from app.repositories.documents import create_document

        session = _make_fake_session()
        explicit_id = uuid.uuid4()

        doc = await create_document(
            session,
            title="Explicit ID",
            source_type="report",
            access_level="public",
            minio_bucket="rd-documents",
            minio_object_key="documents/uuid/doc.txt",
            checksum="def",
            document_id=explicit_id,
        )

        assert doc.id == explicit_id


# ── Schema validation ───────────────────────────────────────────────────


class TestDocumentResponseSchema:
    def test_from_attributes_mode_enabled(self):
        from app.schemas.documents import DocumentResponse

        assert DocumentResponse.model_config.get("from_attributes") is True

    def test_required_fields(self):
        from app.schemas.documents import DocumentResponse

        # language and year are optional — the rest are required.
        fields = DocumentResponse.model_fields
        assert fields["id"].is_required()
        assert fields["title"].is_required()
        assert fields["source_type"].is_required()
        assert fields["access_level"].is_required()
        assert fields["minio_bucket"].is_required()
        assert fields["minio_object_key"].is_required()
        assert fields["checksum"].is_required()
        assert not fields["language"].is_required()
        assert not fields["year"].is_required()
