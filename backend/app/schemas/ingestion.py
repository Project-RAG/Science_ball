from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class IngestionJobResponse(BaseModel):
    """API response for an ingestion job status."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    document_id: uuid.UUID
    status: str
    progress: float | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime

class RetryRequest(BaseModel):
    """Minimal request body for triggering a job retry."""
    pass
