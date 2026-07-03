# TASK_002_docker_compose_and_settings

## Goal

Add Docker Compose and centralized environment settings for MVP infrastructure without implementing storage logic yet.

This task makes the project ready to run the backend together with infrastructure services in local development.

---

## Input context

Read before coding:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- `docs/tasks/TASK_001_backend_skeleton.md`
- this task file

Relevant SDD areas:

- Docker Compose services: backend, worker, postgres, elasticsearch, neo4j, redis, minio.
- Security: secrets only in `.env`.
- YandexGPT environment variables must be backend/worker only.
- MVP deployment on one machine via Docker Compose.

---

## Files to create or change

Expected files:

```text
docker-compose.yml
.env.example
.gitignore
Makefile
backend/Dockerfile
backend/app/settings.py
```

Optional if needed:

```text
backend/.dockerignore
```

---

## Requirements

Add Docker Compose services for MVP infrastructure:

- `backend`
- `worker` as placeholder/runtime peer if practical
- `postgres`
- `elasticsearch`
- `neo4j`
- `redis`
- `minio`

Frontend is not required in this task.

Settings must include environment variables for:

- app name/env/debug;
- backend host/port if needed;
- PostgreSQL;
- Redis;
- Elasticsearch;
- Neo4j;
- MinIO;
- LLM provider;
- YandexGPT placeholders;
- local LLM fallback placeholders.

`.env.example` must contain placeholders only.

`.gitignore` must ignore:

```text
.env
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
*.pyc
```

Docker rules:

- no real secrets;
- use variable expansion from `.env`;
- do not bake secrets into Docker image;
- backend and worker receive LLM env vars only as environment variables;
- healthchecks are welcome but should remain practical.

---

## Explicitly do not do

Do not:

- implement storage client modules;
- add database models;
- add Alembic migrations;
- implement upload;
- implement ingestion tasks;
- implement Elasticsearch mappings;
- implement Neo4j constraints;
- implement LLMGateway;
- add frontend service unless explicitly necessary as placeholder;
- commit `.env`;
- put real Yandex API key anywhere;
- change `docs/SDD.md`.

---

## Validation commands

From repository root:

```bash
docker compose config
```

If Docker is available and dependencies are sufficient:

```bash
docker compose up -d --build postgres redis minio elasticsearch neo4j
```

Backend validation from previous task should still pass:

```bash
cd backend
python -m pytest
```

---

## Definition of Done

- `docker-compose.yml` parses with `docker compose config`.
- `.env.example` contains all required variables with placeholders only.
- `.env` is ignored by git.
- Backend settings can read compose/env variables.
- Backend skeleton tests still pass.
- No storage business logic is implemented prematurely.
- No secrets are present.
- `docs/HANDOFF.md` is updated by Gemma.

---

## Expected handoff update

Gemma must update:

- services added;
- settings added;
- validation command results;
- Docker availability notes;
- any service startup issues;
- next task: `TASK_003_storage_clients.md`;
- commit readiness.

---

## Prompt for DeepSeek in Kodik

```markdown
Ты работаешь в Kodik над проектом R&D Knowledge Map.

Текущая задача: `docs/tasks/TASK_002_docker_compose_and_settings.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- `docs/tasks/TASK_002_docker_compose_and_settings.md`

Сгенерируй только Docker Compose, env example, Dockerfile/settings изменения, необходимые для TASK_002.

Запрещено:
- реализовывать storage clients;
- создавать SQLAlchemy models/Alembic;
- реализовывать upload/ingestion/search/LLM/frontend;
- менять `docs/SDD.md`;
- добавлять реальные секреты;
- помещать Yandex API key во frontend, Docker image или git.

Требования:
- docker compose должен включать backend, worker placeholder/runtime, postgres, elasticsearch, neo4j, redis, minio;
- `.env.example` только с placeholder values;
- `.env` должен быть в `.gitignore`;
- backend settings должны читать новые переменные;
- предыдущие тесты backend не должны ломаться.

В конце выдай:
1. список файлов;
2. команды проверки;
3. какие env vars добавлены;
4. что должен проверить Gemma.
```

---

## Prompt for Gemma-4-31B in Claude Code

```markdown
Ты интегратор проекта R&D Knowledge Map.

Интегрируй результат DeepSeek по `docs/tasks/TASK_002_docker_compose_and_settings.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- текущий git diff

Твоя задача:
- проверить, что Docker/env изменения соответствуют TASK_002;
- исправить compose syntax, Dockerfile, settings, dependency issues;
- убедиться, что `.env` игнорируется;
- убедиться, что `.env.example` не содержит реальных секретов;
- не реализовывать storage clients/models/upload/search/LLM/frontend;
- не менять `docs/SDD.md`;
- запустить проверки;
- обновить `docs/HANDOFF.md`.

Запусти по возможности:

```bash
docker compose config
cd backend && python -m pytest
```

В handoff запиши:
- Docker services;
- env variables;
- validation results;
- known issues;
- next task `TASK_003_storage_clients.md`;
- commit readiness.
```
