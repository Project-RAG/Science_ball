from __future__ import annotations

import time
import uuid
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.worker.celery_app import celery_app
from app.settings import settings

# Setup synchronous DB connection for the Celery worker
sync_engine = create_engine(settings.database_url.replace("postgresql+asyncpg", "postgresql"))
SessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)

logger = logging.getLogger(__name__)

@celery_app.task(name="ingestion.process_document", bind=True)
def process_document_ingestion(self, job_id: str):
    """
    Placeholder for the document ingestion pipeline.
    Simulates the transition from pending -> running -> succeeded/failed.
    """
    job_uuid = uuid.UUID(job_id)
    session = SessionLocal()

    try:
        # 1. Update status to 'running'
        with session.begin():
            session.execute(
                text("UPDATE ingestion_jobs SET status = :status, progress = :progress WHERE id = :id"),
                {"status": "running", "progress": 0.0, "id": job_uuid}
            )

        # 2. Simulate pipeline steps (Placeholder)
        steps = [
            ("Parsing text...", 0.25),
            ("Extracting entities...", 0.50),
            ("Normalizing units...", 0.75),
            ("Indexing to ES/Neo4j...", 1.0),
        ]

        for description, progress in steps:
            time.sleep(3) # Simulate work
            with session.begin():
                session.execute(
                    text("UPDATE ingestion_jobs SET status = :status, progress = :progress WHERE id = :id"),
                    {"status": "running", "progress": progress, "id": job_uuid}
                )
            logger.info(f"Job {job_id}: {description} ({int(progress*100)}%)")

        # 3. Finalize status to succeeded
        with session.begin():
            session.execute(
                text("UPDATE ingestion_jobs SET status = :status, progress = :progress WHERE id = :id"),
                {"status": "succeeded", "progress": 1.0, "id": job_uuid}
            )
        logger.info(f"Job {job_id}: successfully completed.")

    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        with session.begin():
            session.execute(
                text("UPDATE ingestion_jobs SET status = :status, error_message = :err WHERE id = :id"),
                {"status": "failed", "err": str(e), "id": job_uuid}
            )
    finally:
        session.close()

    return {"job_id": job_id, "status": "completed"}
