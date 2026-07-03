# TASK_017_search_api_basic

## Goal

Implement Elasticsearch-backed search API with access filtering and evidence results.

---

## Input context

Read before coding:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- previous task files as applicable
- this task file

Relevant context:

- previous task files 001-016
- SDD hybrid search and access_level requirements

---

## Files to create or change

Expected files:

- `backend/app/api/routes/search.py`
- `backend/app/api/router.py`
- `backend/app/search/search_service.py`
- `backend/app/search/query_builder.py`
- `backend/app/schemas/search.py`
- `backend/tests/unit/test_search_query_builder.py`
- `backend/tests/unit/test_search_api.py`

Add minimal supporting files only when required by imports/tests.

---

## Requirements

- Expose `POST /api/v1/search`.
- Apply mandatory `access_level` filtering.
- Support text query, source type/year/entity/numeric filters at MVP level.
- Return ranked chunks/evidence with document metadata and traceability ids.
- Keep route thin and use service/query builder.

---

## Explicitly do not do

Do not:

- generate LLM answers
- write graph traversal
- skip access filtering
- return hidden documents
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

- Search query builder is tested.
- API response includes evidence and sources.
- `access_level` filter is always present.
- No LLM call is made by basic search.
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
- next task: `TASK_018_answer_synthesis_with_evidence.md`;
- commit readiness.

---

## Prompt for Claude Code with Gemma-4-31B

```markdown
Ты работаешь в Claude Code с моделью Gemma-4-31B над проектом R&D Knowledge Map.

Текущая задача: `docs/tasks/TASK_017_search_api_basic.md`.

Эта задача является продолжением предыдущих задач. Работай так, чтобы результат текущей задачи становился входом для следующей.

Перед началом прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- все предыдущие task-файлы, которые влияют на текущую задачу
- `docs/tasks/TASK_017_search_api_basic.md`

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
- exact next task: `TASK_018_answer_synthesis_with_evidence.md`;
- what the next task should reuse from this task.

После обновления handoff выдай краткий итог:
1. что реализовано;
2. какие команды проверки прошли/не прошли;
3. какие файлы изменены;
4. что делать в следующей задаче `TASK_018_answer_synthesis_with_evidence.md`.
```
