# TASK_001_backend_skeleton

## Goal

Create a minimal FastAPI backend skeleton that matches the SDD project structure and can be imported/tested locally.

This task establishes the backend application boundary only. It must not implement storage, ingestion, auth, search, LLM, or frontend.

---

## Input context

Read before coding:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- this task file

Relevant SDD areas:

- Backend stack: Python 3.11+, FastAPI, SQLAlchemy, Alembic, Pydantic, Celery, Redis.
- API service routes list.
- Recommended project structure.
- Instruction to keep business logic out of routes.

---

## Files to create or change

Expected files:

```text
backend/
  app/
    __init__.py
    main.py
    settings.py
    dependencies.py
    api/
      __init__.py
      router.py
      routes/
        __init__.py
        health.py
  tests/
    __init__.py
    unit/
      __init__.py
      test_health.py
  pyproject.toml
```

Optional if needed:

```text
backend/README.md
```

---

## Requirements

Implement:

- FastAPI app factory or app instance in `backend/app/main.py`.
- API router in `backend/app/api/router.py`.
- Health route in `backend/app/api/routes/health.py`.
- Settings model in `backend/app/settings.py`.
- Placeholder dependency module in `backend/app/dependencies.py`.
- Basic tests for health endpoint.

Health endpoints should include at least one stable endpoint:

```text
GET /health
```

Prefer also exposing versioned API health:

```text
GET /api/v1/health
```

Response may be simple:

```json
{
  "status": "ok",
  "service": "rd-knowledge-map-backend"
}
```

---

## Explicitly do not do

Do not:

- add Docker Compose;
- add database clients;
- add SQLAlchemy models;
- add Alembic;
- add MinIO upload;
- add Celery worker;
- add Redis integration;
- add Elasticsearch integration;
- add Neo4j integration;
- add auth/RBAC implementation;
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

If dependencies are not installed yet, document the install command used, for example:

```bash
cd backend
python -m pip install -e .[dev]
python -m pytest
```

---

## Definition of Done

- Backend package imports successfully.
- FastAPI app starts/imports without external services.
- `GET /health` test passes.
- Settings load without requiring secrets.
- No storage/LLM/business logic is implemented prematurely.
- No real secrets are present.
- `docs/HANDOFF.md` is updated by Gemma.

---

## Expected handoff update

Gemma must update `docs/HANDOFF.md` with:

- task status;
- changed files;
- validation commands and results;
- dependency installation notes;
- any stubs/placeholders;
- next task: `TASK_002_docker_compose_and_settings.md`;
- commit readiness.

---

## Prompt for DeepSeek in Kodik

```markdown
Ты работаешь в Kodik над проектом R&D Knowledge Map.

Текущая задача: `docs/tasks/TASK_001_backend_skeleton.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- `docs/tasks/TASK_001_backend_skeleton.md`

Сгенерируй минимальный FastAPI backend skeleton строго по текущей задаче.

Разрешено создавать/изменять только backend skeleton files, перечисленные в task.

Запрещено:
- добавлять Docker Compose;
- добавлять реальные storage clients;
- добавлять SQLAlchemy models/Alembic;
- добавлять upload/ingestion/search/LLM/frontend;
- менять `docs/SDD.md`;
- хранить секреты.

Требования:
- FastAPI app должен импортироваться без внешних сервисов;
- должен быть health endpoint;
- должны быть минимальные тесты health endpoint;
- routes должны быть тонкими;
- settings должны загружаться без реальных секретов.

В конце выдай:
1. список созданных/измененных файлов;
2. команды проверки;
3. известные stubs/placeholders;
4. что должен проверить Gemma-интегратор.
```

---

## Prompt for Gemma-4-31B in Claude Code

```markdown
Ты интегратор проекта R&D Knowledge Map.

Интегрируй результат DeepSeek по задаче `docs/tasks/TASK_001_backend_skeleton.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- текущий git diff

Твоя задача:
- проверить, что изменения строго соответствуют TASK_001;
- исправить импорты, зависимости, структуру пакетов, тесты;
- не добавлять Docker/storage/models/upload/search/LLM/frontend;
- не переписывать архитектуру;
- не менять `docs/SDD.md`;
- запустить проверки;
- обновить `docs/HANDOFF.md`.

Запусти по возможности:

```bash
cd backend
python -m pytest
python -m compileall app
```

Если зависимостей не хватает, добавь минимальную корректную dependency-конфигурацию и задокументируй команду установки.

В `docs/HANDOFF.md` запиши:
- changed files;
- validation results;
- stubs/placeholders;
- known issues;
- next task `TASK_002_docker_compose_and_settings.md`;
- можно ли делать commit.
```
