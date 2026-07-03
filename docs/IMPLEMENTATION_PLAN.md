# Implementation Plan

## Principles

- Implement one small task at a time.
- One task should be reviewable and testable independently.
- DeepSeek generates scoped code.
- Gemma integrates and validates.
- Commit after each accepted task.
- Do not edit `docs/SDD.md`.

---

## Phase 1 — Backend foundation

### TASK_001_backend_skeleton

Goal: create minimal FastAPI backend skeleton.

Input context:
- `docs/SDD.md` sections: backend services, API routes, project structure.
- `docs/AI_RULES.md`.

Files to create/change:
- `backend/app/main.py`
- `backend/app/api/router.py`
- `backend/app/api/routes/health.py`
- `backend/app/settings.py`
- `backend/app/dependencies.py`
- `backend/tests/unit/test_health.py`
- `backend/pyproject.toml` or dependency file

Do not:
- add real database clients;
- add Docker Compose;
- add upload logic;
- add auth implementation;
- add LLM code.

Checks:

```bash
cd backend
python -m pytest
python -m compileall app
```

Definition of Done:
- FastAPI app imports;
- health endpoint exists;
- tests pass;
- settings load without secrets.

Expected handoff update:
- backend skeleton status;
- changed files;
- validation result;
- next task `TASK_002_docker_compose_and_settings`.

---

### TASK_002_docker_compose_and_settings

Goal: add Docker Compose and environment settings for MVP infrastructure.

Files:
- `docker-compose.yml`
- `.env.example`
- `.gitignore`
- `backend/Dockerfile`
- `backend/app/settings.py`
- optional `Makefile`

Do not:
- hardcode secrets;
- implement storage clients;
- implement migrations;
- implement frontend.

Checks:

```bash
docker compose config
```

Definition of Done:
- compose config validates;
- all service env vars use placeholders or `.env` expansion;
- `.env` ignored by git.

Expected handoff update:
- listed services;
- env variables added;
- any services not started locally.

---

### TASK_003_storage_clients

Goal: add basic storage client factories for PostgreSQL, Redis, Elasticsearch, Neo4j, MinIO.

Files:
- `backend/app/db/postgres.py`
- `backend/app/db/redis.py`
- `backend/app/db/elasticsearch.py`
- `backend/app/db/neo4j.py`
- `backend/app/db/minio.py`
- `backend/app/api/routes/health.py`
- tests for client config/init with mocks where practical

Do not:
- create SQLAlchemy models;
- create Alembic migrations;
- implement upload;
- create Elasticsearch mappings;
- write Neo4j graph logic.

Checks:

```bash
cd backend
python -m pytest
python -m compileall app
```

Definition of Done:
- clients can be constructed from settings;
- health route can expose basic app status without requiring all services to be live;
- no secrets logged.

Expected handoff update:
- client modules added;
- connection behavior;
- stubs/mocks.

---

### TASK_004_postgres_models_and_alembic

Goal: add SQLAlchemy base models and Alembic setup for core transactional tables.

Files:
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/versions/...`
- `backend/app/models/base.py`
- `backend/app/models/document.py`
- `backend/app/models/ingestion_job.py`
- `backend/app/models/chunk.py`
- `backend/app/models/fact.py`
- `backend/app/models/audit_log.py`
- tests/migration sanity checks if practical

Do not:
- implement upload endpoint;
- implement fact review workflow;
- implement auth/RBAC fully;
- implement Elasticsearch indexing.

Checks:

```bash
cd backend
alembic upgrade head
python -m pytest
```

Definition of Done:
- migration creates core tables;
- document/chunk/fact tables contain traceability and `access_level` where required;
- no binary files stored in PostgreSQL.

Expected handoff update:
- migration id;
- tables created;
- any schema compromises.

---

### TASK_005_document_upload_minio

Goal: implement MVP document upload to MinIO plus PostgreSQL metadata row.

Files:
- `backend/app/api/routes/documents.py`
- `backend/app/schemas/documents.py`
- `backend/app/services/ingestion/document_upload_service.py`
- `backend/app/repositories/documents.py`
- `backend/app/db/minio.py`
- tests for upload service/API with mocks

Do not:
- parse documents;
- chunk text;
- run Celery ingestion;
- index into Elasticsearch;
- write Neo4j graph;
- call LLM.

Checks:

```bash
cd backend
python -m pytest
```

Definition of Done:
- `POST /api/v1/documents/upload` accepts allowed file types for MVP;
- original file stored in MinIO;
- metadata stored in PostgreSQL;
- checksum recorded;
- `access_level` recorded;
- upload does not expose secrets.

Expected handoff update:
- endpoint behavior;
- file type limits;
- stubs for future parsing/ingestion.

---

## Phase 2 — Ingestion MVP

### TASK_006_ingestion_job_status

Goal: add ingestion job model usage, job status API, and Celery task placeholder.

Do not parse documents yet.

Checks:

```bash
cd backend
python -m pytest
```

Definition of Done:
- upload can create or reference ingestion job;
- job status endpoint returns pending/running/succeeded/failed;
- Celery task placeholder is wired but minimal.

---

### TASK_007_text_parsers

Goal: implement parsers for TXT, Markdown, PDF, DOCX MVP.

Do not chunk/index/extract facts yet.

Definition of Done:
- parser service returns text and basic metadata;
- tests use sample small files.

---

### TASK_008_chunking_service

Goal: implement deterministic text chunking with document/chunk traceability.

Definition of Done:
- chunks persisted to PostgreSQL;
- each chunk has `document_id`, order/index, text, optional page/section, `access_level`.

---

## Phase 3 — NLP MVP

### TASK_009_dictionary_entity_extraction

Goal: extract domain entities using ontology dictionaries.

Definition of Done:
- Material/Process/Equipment extraction works with aliases;
- no LLM dependency.

### TASK_010_numeric_extractor_and_units

Goal: extract numeric conditions via regex/parser and normalize units.

Definition of Done:
- temperature, pH, flow velocity, pressure, concentration examples tested;
- raw text and normalized values preserved.

### TASK_011_confidence_service

Goal: implement MVP confidence scoring.

Definition of Done:
- facts get confidence based on deterministic formula inputs;
- LLM-only cap rule represented for later LLM use.

---

## Phase 4 — Indexing and graph

### TASK_012_elasticsearch_mappings

Goal: create Elasticsearch index mappings for docs, chunks, entities, facts.

Definition of Done:
- mappings contain `access_level`;
- numeric fields and nested numeric conditions are represented;
- vector dimension is configurable.

### TASK_013_indexing_chunks_and_facts

Goal: index documents/chunks/facts into Elasticsearch.

Definition of Done:
- indexing service writes searchable evidence;
- access level is included in all docs.

### TASK_014_neo4j_graph_writer

Goal: write basic graph nodes/edges from extracted facts.

Definition of Done:
- constraints created;
- graph edges contain fact/source metadata.

---

## Phase 5 — LLM integration

### TASK_015_llm_gateway_mock_and_yandex

Goal: implement provider abstraction, mock provider, Yandex provider shell.

Definition of Done:
- business code uses `LLMGateway`;
- tests use `MockLLMProvider`;
- secrets only from env.

### TASK_016_query_understanding

Goal: implement query understanding with YandexGPT through gateway and deterministic fallback.

Definition of Done:
- output validated with Pydantic;
- fallback works when LLM fails.

---

## Phase 6 — Search and answers

### TASK_017_search_api_basic

Goal: implement Elasticsearch-backed search with access filtering.

Definition of Done:
- query applies `access_level` filter;
- returns ranked chunks/evidence.

### TASK_018_answer_synthesis_with_evidence

Goal: generate answers only from evidence through `LLMGateway`.

Definition of Done:
- no evidence means no invented answer;
- response includes sources/confidence/gaps.

---

## Phase 7 — Verification and frontend MVP

### TASK_019_fact_review_api

Goal: implement pending/verify/reject/comment fact APIs with versioning.

### TASK_020_frontend_document_upload

Goal: add upload screen.

### TASK_021_frontend_search_and_answer

Goal: add search and answer display.

### TASK_022_frontend_graph_preview

Goal: add basic graph preview.

---

## Phase 8 — Demo polish

### TASK_023_markdown_export

Goal: export answer to Markdown.

### TASK_024_demo_data_and_script

Goal: add sample data and demo script.

---

## Open Questions

| ID | Question | MVP path |
|---|---|---|
| OQ-001 | SDD contains duplicated/garbled fragments. | Use clean repeated intent, do not edit SDD. |
| OQ-002 | Exact upload limits are unspecified. | Add configurable conservative defaults. |
| OQ-003 | Full auth/RBAC timing is unclear. | Preserve `access_level` from the start, implement auth later. |
| OQ-004 | Embedding dimensions depend on provider. | Make dimension configurable and version indices. |
