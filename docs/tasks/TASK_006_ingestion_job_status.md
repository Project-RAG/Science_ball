# TASK_006_ingestion_job_status

## Goal

Add ingestion job creation/status tracking and a minimal Celery task boundary for document processing.

---

## Input context

Read before coding:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- previous task files as applicable
- this task file

Relevant context:

- previous task files 001-005
- SDD ingestion pipeline, Redis/Celery, PostgreSQL ingestion jobs

---

## Files to create or change

Expected files:

- `backend/app/api/router.py`
- `backend/app/api/routes/ingestion.py`
- `backend/app/schemas/ingestion.py`
- `backend/app/services/ingestion/job_service.py`
- `backend/app/repositories/ingestion_jobs.py`
- `backend/app/worker/__init__.py`
- `backend/app/worker/celery_app.py`
- `backend/app/worker/tasks.py`
- `backend/app/models/ingestion_job.py`
- `backend/tests/unit/test_ingestion_job_service.py`

Add minimal supporting files only when required by imports/tests.

---

## Requirements

- Create or reuse ingestion job row when a document is uploaded or submitted for ingestion.
- Expose `GET /api/v1/ingestion/jobs/{job_id}`.
- Expose `POST /api/v1/ingestion/jobs/{job_id}/enqueue` or equivalent minimal trigger.
- Define job statuses: pending, queued, running, succeeded, failed.
- Wire Celery app and placeholder task without parsing documents yet.
- Keep routes thin; use service/repository layers.

---

## Explicitly do not do

Do not:

- parse documents
- chunk text
- index Elasticsearch
- write Neo4j graph
- call LLM
- implement frontend
- change `docs/SDD.md`
- commit real secrets or private data

---

## Validation commands

From repository root, adapt to the current stage:

```bash
cd backend
python -m pytest
python -m compileall app
```

If frontend files are changed:

```bash
cd frontend
npm install
npm run build
```

If Docker services are required and available:

```bash
docker compose up -d
```

---

## Definition of Done

- Job status API returns current state.
- Upload flow can reference or create ingestion job.
- Celery task boundary exists and can be imported.
- Tests cover job service/status behavior with mocks/fakes.
- No parsing/chunking/indexing/LLM work is implemented prematurely.
- `docs/HANDOFF.md` is updated by Claude Code with Gemma-4-31B.

---

## Expected handoff update

Claude Code with Gemma-4-31B must update `docs/HANDOFF.md` with:

- task status;
- changed files;
- validation commands and results;
- runtime notes;
- stubs/placeholders;
- known issues;
- next task: `TASK_007_text_parsers.md`;
- commit readiness.

---

## Prompt for Claude Code with Gemma-4-31B

```markdown
Ты работаешь в Claude Code с моделью Gemma-4-31B над проектом R&D Knowledge Map.

Текущая задача: `docs/tasks/TASK_006_ingestion_job_status.md`.

Эта задача является продолжением предыдущих задач. Работай так, чтобы результат текущей задачи становился входом для следующей.

Перед началом прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- все предыдущие task-файлы, которые влияют на текущую задачу
- `docs/tasks/TASK_006_ingestion_job_status.md`

Обязательно проверь текущее состояние проекта:
- `git status`
- текущий diff
- уже созданные backend/frontend файлы
- заметки и known issues из `docs/HANDOFF.md`

Твоя задача:
1. Реализовать только scope текущей задачи.
2. Сохранить совместимость с результатами предыдущих задач.
3. Не реализовывать будущие задачи преждевременно.
4. Держать routes тонкими: HTTP слой только валидирует/вызывает service layer.
5. Держать storage/API/LLM доступ за services, repositories, clients или gateway abstractions.
6. Не менять `docs/SDD.md`.
7. Не добавлять реальные секреты, приватные документы или токены.
8. Добавить/обновить тесты для текущей задачи.
9. Запустить релевантные проверки.
10. Обновить `docs/HANDOFF.md` так, чтобы следующая задача могла начаться без дополнительного контекста.

Минимальные проверки для backend-задач:

```bash
cd backend
python -m pytest
python -m compileall app
```

Если задача меняет frontend:

```bash
cd frontend
npm install
npm run build
```

Если задача требует инфраструктуру и Docker доступен:

```bash
docker compose config
docker compose up -d
```

В конце обнови `docs/HANDOFF.md` в формате:
- completed task;
- implemented behavior;
- changed files;
- validation commands and results;
- runtime/startup notes;
- stubs/placeholders intentionally left;
- known issues or blockers;
- exact next task: `TASK_007_text_parsers.md`;
- what the next task should reuse from this task.

После обновления handoff выдай краткий итог:
1. что реализовано;
2. какие команды проверки прошли/не прошли;
3. какие файлы изменены;
4. что делать в следующей задаче `TASK_007_text_parsers.md`.
```
