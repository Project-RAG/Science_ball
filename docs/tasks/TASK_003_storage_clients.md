# TASK_003_storage_clients

## Goal

Add basic backend client/session factory modules for external storage systems:

- PostgreSQL
- Redis
- Elasticsearch
- Neo4j
- MinIO

The goal is configuration and safe construction only. Do not implement domain persistence, indexing, graph writing, or upload workflows yet.

---

## Input context

Read before coding:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- `docs/tasks/TASK_001_backend_skeleton.md`
- `docs/tasks/TASK_002_docker_compose_and_settings.md`
- this task file

Relevant SDD areas:

- PostgreSQL is transactional source of truth.
- Elasticsearch is primary search layer.
- Neo4j is graph traversal layer.
- MinIO stores source files/artifacts/exports.
- Redis supports queues/cache/job status.
- External system access must be separated from API routes.

---

## Files to create or change

Expected files:

```text
backend/app/db/__init__.py
backend/app/db/postgres.py
backend/app/db/redis.py
backend/app/db/elasticsearch.py
backend/app/db/neo4j.py
backend/app/db/minio.py
backend/app/api/routes/health.py
backend/app/settings.py
backend/tests/unit/test_storage_clients.py
```

Optional if useful:

```text
backend/app/db/errors.py
```

---

## Requirements

Implement minimal construction helpers:

- PostgreSQL SQLAlchemy engine/session factory or async equivalent, based on current project style.
- Redis client factory.
- Elasticsearch client factory.
- Neo4j driver factory.
- MinIO client factory.

Health route may expose app health and optionally dependency configuration status, but must not fail just because local external services are down unless explicitly designed as deep health.

Client modules must:

- read from centralized settings;
- avoid logging secrets;
- not connect eagerly in a way that breaks app import;
- be testable with mocks or construction-only tests.

---

## Explicitly do not do

Do not:

- create SQLAlchemy models;
- create Alembic migrations;
- implement document repositories;
- implement upload endpoint;
- implement MinIO bucket creation workflow unless only a harmless helper;
- create Elasticsearch mappings;
- write Neo4j constraints;
- add Celery tasks;
- add LLMGateway;
- add frontend;
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
docker compose up -d postgres redis minio elasticsearch neo4j
```

But tests should not require live services unless marked integration.

---

## Definition of Done

- Storage client modules exist.
- App imports without live external services.
- Client factories use settings.
- Unit tests validate construction/config behavior without real secrets.
- Health endpoint remains available.
- No domain persistence/indexing/graph/upload logic is implemented prematurely.
- `docs/HANDOFF.md` is updated by Gemma.

---

## Expected handoff update

Gemma must update:

- client modules added;
- dependency packages added;
- validation results;
- whether tests use mocks;
- any external service startup notes;
- next task: `TASK_004_postgres_models_and_alembic.md`;
- commit readiness.

---

## Prompt for DeepSeek in Kodik

```markdown
Ты работаешь в Kodik над проектом R&D Knowledge Map.

Текущая задача: `docs/tasks/TASK_003_storage_clients.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- `docs/tasks/TASK_003_storage_clients.md`

Сгенерируй минимальные storage client/session factory modules для PostgreSQL, Redis, Elasticsearch, Neo4j и MinIO.

Запрещено:
- создавать SQLAlchemy models;
- создавать Alembic migrations;
- реализовывать upload/ingestion/search/indexing/graph writing/LLM/frontend;
- вызывать внешние сервисы при import приложения;
- логировать секреты;
- менять `docs/SDD.md`.

Требования:
- все clients читают настройки из `backend/app/settings.py`;
- app import не должен требовать поднятых сервисов;
- tests должны использовать construction/mocks, не live credentials;
- routes остаются тонкими.

В конце выдай:
1. список файлов;
2. добавленные зависимости;
3. команды проверки;
4. stubs/limitations для Gemma.
```

---

## Prompt for Gemma-4-31B in Claude Code

```markdown
Ты интегратор проекта R&D Knowledge Map.

Интегрируй результат DeepSeek по `docs/tasks/TASK_003_storage_clients.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- текущий git diff

Твоя задача:
- проверить, что добавлены только storage client factories;
- исправить dependencies/imports/settings/tests;
- убедиться, что app импортируется без live services;
- убедиться, что секреты не логируются и не hardcoded;
- не добавлять models/migrations/upload/search/LLM/frontend;
- не менять `docs/SDD.md`;
- запустить проверки;
- обновить `docs/HANDOFF.md`.

Запусти:

```bash
cd backend
python -m pytest
python -m compileall app
```

В handoff запиши:
- client modules;
- dependency changes;
- validation results;
- stubs/mocks;
- next task `TASK_004_postgres_models_and_alembic.md`;
- commit readiness.
```
