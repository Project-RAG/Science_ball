# TASK_021_frontend_search_and_answer

## Goal

Add frontend search and grounded answer UI.

---

## Input context

Read before coding:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- previous task files as applicable
- this task file

Relevant context:

- previous task files 001-020
- SDD search and answer UX requirements

---

## Files to create or change

Expected files:

- `frontend/src/api/search.ts`
- `frontend/src/api/answers.ts`
- `frontend/src/features/search/SearchPage.tsx`
- `frontend/src/features/search/SearchResults.tsx`
- `frontend/src/features/answers/AnswerPanel.tsx`
- `frontend/src/App.tsx`

Add minimal supporting files only when required by imports/tests.

---

## Requirements

- Provide search input and basic filters.
- Call `POST /api/v1/search` and render evidence results.
- Call answer endpoint and render answer with sources/confidence/gaps.
- Show loading/error/empty states.
- Keep backend base URL configurable.

---

## Explicitly do not do

Do not:

- call LLM directly from frontend
- store tokens in browser code
- implement graph preview
- hide source references
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

- User can search and see evidence.
- User can request answer and see sources.
- No direct external LLM calls exist in frontend.
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
- next task: `TASK_022_frontend_graph_preview.md`;
- commit readiness.

---

## Prompt for Claude Code with Gemma-4-31B

```markdown
Ты работаешь в Claude Code с моделью Gemma-4-31B над проектом R&D Knowledge Map.

Текущая задача: `docs/tasks/TASK_021_frontend_search_and_answer.md`.

Эта задача является продолжением предыдущих задач. Работай так, чтобы результат текущей задачи становился входом для следующей.

Перед началом прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- все предыдущие task-файлы, которые влияют на текущую задачу
- `docs/tasks/TASK_021_frontend_search_and_answer.md`

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
- exact next task: `TASK_022_frontend_graph_preview.md`;
- what the next task should reuse from this task.

После обновления handoff выдай краткий итог:
1. что реализовано;
2. какие команды проверки прошли/не прошли;
3. какие файлы изменены;
4. что делать в следующей задаче `TASK_022_frontend_graph_preview.md`.
```
