# TASK_004_postgres_models_and_alembic

## Goal

Add SQLAlchemy models and Alembic setup for core PostgreSQL transactional tables required by the SDD.

This task creates schema foundation only. It must not implement upload or ingestion workflows yet.

---

## Input context

Read before coding:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- previous task files 001-003
- this task file

Relevant SDD areas:

- PostgreSQL design.
- Required tables: users, roles, user_roles, documents, document_versions, ingestion_jobs, chunks, entities, facts, fact_versions, fact_reviews, audit_log, saved_queries, notifications, exports.
- MVP can start with core subset, but must preserve extension path.
- Documents/chunks/facts require access/tracing fields.

---

## Files to create or change

Expected files:

```text
backend/alembic.ini
backend/alembic/env.py
backend/alembic/script.py.mako
backend/alembic/versions/<revision>_initial_core_tables.py
backend/app/models/__init__.py
backend/app/models/base.py
backend/app/models/document.py
backend/app/models/ingestion_job.py
backend/app/models/chunk.py
backend/app/models/fact.py
backend/app/models/audit_log.py
backend/app/db/postgres.py
backend/tests/unit/test_models.py
```

Optional if scope remains small:

```text
backend/app/models/user.py
backend/app/models/role.py
backend/app/models/export.py
```

---

## Required core tables for this task

Implement at least:

- `documents`
- `document_versions` if simple enough, otherwise document in handoff for next schema task
- `ingestion_jobs`
- `chunks`
- `entities` if simple enough
- `facts`
- `fact_versions`
- `fact_reviews` if simple enough
- `audit_log`

Minimum required fields:

### documents

- `id` UUID primary key
- `title`
- `source_type`
- `language`
- `year`
- `access_level`
- `minio_bucket`
- `minio_object_key`
- `checksum`
- `created_by`
- `created_at`
- `updated_at`

### chunks

- `id` UUID primary key
- `document_id`
- `chunk_index`
- `text`
- `language`
- `page`
- `section`
- `access_level`
- `created_at`

### facts

- `id` UUID primary key
- `subject_id`
- `subject_type`
- `predicate`
- `object_id`
- `object_type`
- `source_document_id`
- `source_chunk_id`
- `confidence`
- `verification_status`
- `created_by`
- `created_at`
- `updated_at`

### fact_versions

- `id` UUID primary key
- `fact_id`
- `version`
- `payload` JSON/JSONB
- `changed_by`
- `change_reason`
- `created_at`

### audit_log

- `id` UUID primary key
- `user_id`
- `action`
- `entity_type`
- `entity_id`
- `payload` JSON/JSONB
- `created_at`

---

## Explicitly do not do

Do not:

- implement document upload endpoint;
- implement repositories beyond what is necessary for model tests;
- implement file parsing;
- implement Celery ingestion;
- implement Elasticsearch indexing;
- implement Neo4j graph writing;
- implement fact review API;
- implement auth/RBAC logic beyond nullable user fields or simple tables;
- call LLM;
- change `docs/SDD.md`.

---

## Validation commands

From repository root:

```bash
cd backend
alembic upgrade head
python -m pytest
python -m compileall app
```

If no live PostgreSQL is available, Gemma may validate migration generation/import and document that full DB migration was not run.

---

## Definition of Done

- Alembic is configured against the app metadata.
- Core SQLAlchemy models exist.
- Initial migration exists.
- Migration creates core tables.
- `documents`, `chunks`, and `facts` preserve traceability and `access_level` requirements.
- No binary files are stored in PostgreSQL.
- Existing backend tests still pass.
- `docs/HANDOFF.md` is updated by Gemma.

---

## Expected handoff update

Gemma must update:

- migration revision id;
- tables implemented;
- tables postponed, if any;
- validation results;
- database availability notes;
- next task: `TASK_005_document_upload_minio.md`;
- commit readiness.

---

## Prompt for DeepSeek in Kodik

```markdown
Ты работаешь в Kodik над проектом R&D Knowledge Map.

Текущая задача: `docs/tasks/TASK_004_postgres_models_and_alembic.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- `docs/tasks/TASK_004_postgres_models_and_alembic.md`

Сгенерируй SQLAlchemy models и Alembic setup для core PostgreSQL tables по TASK_004.

Запрещено:
- реализовывать upload endpoint;
- реализовывать repositories/workflows beyond schema basics;
- реализовывать parsing/chunking/indexing/graph/LLM/frontend;
- хранить binary files в PostgreSQL;
- менять `docs/SDD.md`.

Требования:
- Alembic должен использовать metadata моделей приложения;
- documents/chunks/facts должны иметь traceability/access fields;
- facts должны ссылаться на source document/chunk fields;
- migration должна быть минимальной и читаемой;
- tests должны быть focused и не требовать внешнего LLM.

В конце выдай:
1. список файлов;
2. migration revision;
3. команды проверки;
4. schema limitations/postponed tables для Gemma.
```

---

## Prompt for Gemma-4-31B in Claude Code

```markdown
Ты интегратор проекта R&D Knowledge Map.

Интегрируй результат DeepSeek по `docs/tasks/TASK_004_postgres_models_and_alembic.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- текущий git diff

Твоя задача:
- проверить модели и Alembic setup;
- исправить imports, metadata wiring, migration, dependency issues;
- убедиться, что documents/chunks/facts имеют access_level/traceability fields;
- не реализовывать upload/ingestion/search/graph/LLM/frontend;
- не менять `docs/SDD.md`;
- запустить проверки;
- обновить `docs/HANDOFF.md`.

Запусти по возможности:

```bash
cd backend
alembic upgrade head
python -m pytest
python -m compileall app
```

Если PostgreSQL не поднят, проверь хотя бы imports/tests и запиши ограничение в handoff.

В handoff запиши:
- migration revision;
- tables created;
- validation results;
- known issues;
- next task `TASK_005_document_upload_minio.md`;
- commit readiness.
```
