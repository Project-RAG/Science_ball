# HANDOFF

## Current status

- Current task: `TASK_009_dictionary_entity_extraction`
- Status: completed
- Last updated by: Gemma (Integrator)
- Last updated at: 2026-07-03

---

## Completed tasks

| Task | Status | Notes |
|---|---|---|
| TASK_000_project_orchestration_docs | completed | Orchestration docs created |
| TASK_001_backend_skeleton | completed | FastAPI skeleton implemented and verified |
| TASK_002_docker_compose_and_settings | completed | Infrastructure Dockerized, env settings centralized |
| TASK_003_storage_clients | completed | Storage client factories implemented |
| TASK_004_postgres_models_and_alembic | completed | SQLAlchemy models and Alembic migrations setup |
| TASK_005_document_upload_minio | completed | Document upload to MinIO implemented |
| TASK_006_ingestion_job_status | completed | Ingestion job tracking and status API implemented |
| TASK_007_text_parsers | completed | MVP text extraction for TXT, MD, PDF, DOCX, CSV, XLSX implemented |
| TASK_008_chunking_service | completed | Deterministic sliding window chunking with persistence implemented |
| TASK_009_dictionary_entity_extraction | completed | Dictionary-based entity extraction (Material, Process, etc.) implemented |

---

## Current repository state

### Implemented
- Document upload and metadata persistence.
- Ingestion job lifecycle management (Celery tasks).
- Text Parsing Service:
    - `ParsingService` dispatcher.
    - Support for TXT, MD, PDF, DOCX, CSV, XLSX.
- Text Chunking Service:
    - `ChunkingService`: Deterministic sliding window chunking.
    - `ChunksRepository`: Persistence in PostgreSQL.
- Entity Extraction Service (NLP MVP):
    - `EntityExtractor`: Deterministic matching using domain dictionaries and aliases.
    - `EntityExtractionService`: Orchestrates extraction for document chunks with idempotency.
    - `EntitiesRepository`: Persistence of extracted entities tied to documents and chunks.
    - Domain dictionary supporting Material, Process, Equipment, Property, Organization, Location.

### Not implemented yet
- Numeric extraction and unit normalization.
- Confidence scoring for facts.
- Indexing to Elasticsearch and Neo4j.
- LLM integration via Gateway.
- Frontend.

---

## Changed files in latest task

```text
backend/app/services/nlp/__init__.py
backend/app/services/nlp/dictionaries.py
backend/app/services/nlp/entity_extractor.py
backend/app/services/nlp/entity_extraction_service.py
backend/app/repositories/entities.py
backend/tests/unit/test_entity_extractor.py
```

---

## Validation commands run

```bash
python -m pytest tests/unit/test_entity_extractor.py
python -m compileall app
```

Result:
- `pytest`: 4 passed (covered basic extraction, alias resolution, longest match preference, and service integration).
- `compileall`: Success.

---

## Stubs and mocks

| Area | Stub/mock | Reason | Removal task |
|---|---|---|---|
| Tabular Data | pandas `.to_string()` | Simplified text representation for MVP | TASK_013+ (during indexing) |
| PDF Pages | `[Page X]` markers | Basic structure hint without complex layout analysis | Later refinement |

---

## Known issues

| ID | Issue | Severity | Workaround | Target task |
|---|---|---|---|
| CHUNK-01 | Overlap at end of text | Last chunk may be smaller than `chunk_size`. | N/A | Later refinement |
| ENTITY-01 | Simple Dictionary Match | Only finds exact alias matches (no stemming/lemmatization). | Acceptable for MVP dictionary phase. | Future NLP Refinement |

---

## Open questions

| ID | Question | Practical MVP path | Decision |
|---|---|---|---|
| OQ-004 | Tabular data formatting | Use pandas default string representation for "text" output | Accepted for MVP |

---

## Environment notes

No new external dependencies added. `pytest-asyncio` used in tests.

---

## Next task

Recommended next task:
```text
TASK_010_numeric_extractor_and_units.md
```

Read before and reuse from this task:
- Use the same chunks produced by `ChunkingService`.
- Entities extracted here (like `Property`) will be used as anchors for numeric extraction in the next task.
- Follow the same idempotency pattern (delete old records before re-processing).

---

## Commit readiness

- Ready to commit: yes
- Reason: TASK_009 fully implemented and verified. Entity extraction is deterministic, aliases are supported, and integration with the repository is tested. Traceability to chunks is preserved. No secrets introduced.
