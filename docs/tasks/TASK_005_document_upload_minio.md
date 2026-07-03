# TASK_005_document_upload_minio

## Goal

Implement MVP document upload endpoint that stores the original file in MinIO and writes document metadata to PostgreSQL.

This task implements upload only. Parsing, chunking, Celery ingestion, Elasticsearch indexing, Neo4j graph writing, and LLM calls remain future tasks.

---

## Input context

Read before coding:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- previous task files 001-004
- this task file

Relevant SDD areas:

- Documents API: `POST /api/v1/documents/upload`.
- Ingestion pipeline starts with upload file -> save original to MinIO -> create document metadata in PostgreSQL.
- PostgreSQL `documents` table.
- MinIO stores original documents.
- All documents must have `access_level`.
- Secrets must not be exposed.

---

## Files to create or change

Expected files:

```text
backend/app/api/router.py
backend/app/api/routes/documents.py
backend/app/schemas/__init__.py
backend/app/schemas/documents.py
backend/app/services/__init__.py
backend/app/services/ingestion/__init__.py
backend/app/services/ingestion/document_upload_service.py
backend/app/repositories/__init__.py
backend/app/repositories/documents.py
backend/app/db/minio.py
backend/app/models/document.py
backend/tests/unit/test_document_upload_service.py
```

Optional if needed:

```text
backend/tests/unit/test_documents_api.py
```

---

## Requirements

Implement endpoint:

```text
POST /api/v1/documents/upload
```

The endpoint should accept multipart form upload with metadata such as:

- file;
- title;
- source_type;
- access_level;
- language optional;
- year optional.

MVP allowed file extensions:

- `.pdf`
- `.docx`
- `.txt`
- `.md`
- `.csv`
- `.xlsx`

The upload service should:

1. validate allowed file extension/content name at MVP level;
2. calculate checksum;
3. generate MinIO object key;
4. store original file in MinIO;
5. create document metadata row in PostgreSQL through repository;
6. return document id and metadata;
7. not parse content yet.

Repository should:

- use SQLAlchemy session;
- create document row;
- not store file bytes in PostgreSQL.

MinIO client helper should:

- use settings;
- avoid logging secrets;
- expose upload helper if appropriate.

---

## Explicitly do not do

Do not:

- parse file contents;
- create chunks;
- create ingestion Celery job unless a tiny placeholder already exists and is required;
- index into Elasticsearch;
- write to Neo4j;
- call YandexGPT or any LLM;
- implement frontend upload UI;
- implement full auth/RBAC;
- implement virus scanning/OCR;
- change `docs/SDD.md`.

---

## Validation commands

From repository root:

```bash
cd backend
python -m pytest
python -m compileall app
```

If Docker services are available:

```bash
docker compose up -d postgres minio
cd backend
alembic upgrade head
python -m pytest
```

Optional API smoke after app is running:

```bash
curl -f http://localhost:8000/health
```

---

## Definition of Done

- `POST /api/v1/documents/upload` is registered.
- Upload service stores original file in MinIO via client abstraction.
- Document metadata is stored in PostgreSQL via repository.
- `checksum`, `minio_bucket`, `minio_object_key`, `access_level` are recorded.
- Tests cover service behavior with mocks/fakes.
- No file bytes are stored in PostgreSQL.
- No parsing/chunking/indexing/graph/LLM work is implemented prematurely.
- No secrets are exposed.
- `docs/HANDOFF.md` is updated by Gemma.

---

## Expected handoff update

Gemma must update:

- endpoint implemented;
- metadata fields supported;
- allowed file types;
- test/validation results;
- MinIO/PostgreSQL runtime notes;
- stubs for future parsing/ingestion;
- next task: `TASK_006_ingestion_job_status.md`;
- commit readiness.

---

## Prompt for DeepSeek in Kodik

```markdown
Ты работаешь в Kodik над проектом R&D Knowledge Map.

Текущая задача: `docs/tasks/TASK_005_document_upload_minio.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- `docs/tasks/TASK_005_document_upload_minio.md`

Сгенерируй MVP document upload endpoint, service и repository строго по TASK_005.

Запрещено:
- парсить документы;
- создавать chunks;
- запускать Celery ingestion;
- индексировать Elasticsearch;
- писать Neo4j graph;
- вызывать LLM/YandexGPT;
- делать frontend;
- хранить file bytes в PostgreSQL;
- менять `docs/SDD.md`;
- хранить секреты.

Требования:
- endpoint `POST /api/v1/documents/upload`;
- original file сохраняется в MinIO через client abstraction;
- metadata сохраняется в PostgreSQL через repository;
- записываются checksum, bucket, object key, access_level;
- routes должны быть тонкими;
- tests должны использовать mocks/fakes для MinIO/DB, если live services не нужны.

В конце выдай:
1. список файлов;
2. команды проверки;
3. stubs для будущего parsing/ingestion;
4. что должен проверить Gemma.
```

---

## Prompt for Gemma-4-31B in Claude Code

```markdown
Ты интегратор проекта R&D Knowledge Map.

Интегрируй результат DeepSeek по `docs/tasks/TASK_005_document_upload_minio.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- текущий git diff

Твоя задача:
- проверить upload endpoint/service/repository;
- исправить imports, dependency injection, SQLAlchemy session use, MinIO helper, tests;
- убедиться, что routes тонкие;
- убедиться, что file bytes не сохраняются в PostgreSQL;
- убедиться, что access_level/checksum/minio object metadata записываются;
- не реализовывать parsing/chunking/Celery/indexing/graph/LLM/frontend;
- не менять `docs/SDD.md`;
- запустить проверки;
- обновить `docs/HANDOFF.md`.

Запусти по возможности:

```bash
cd backend
python -m pytest
python -m compileall app
```

Если доступны postgres/minio:

```bash
docker compose up -d postgres minio
cd backend
alembic upgrade head
python -m pytest
```

В handoff запиши:
- endpoint behavior;
- allowed file types;
- validation results;
- stubs/future ingestion notes;
- known issues;
- next task `TASK_006_ingestion_job_status.md`;
- commit readiness.
```
