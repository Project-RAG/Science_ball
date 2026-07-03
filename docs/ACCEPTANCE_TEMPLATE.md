# Stage Acceptance Template

Use this checklist after every task before commit.

## 1. Task identity

- Task file: `docs/tasks/TASK_XXX_...md`
- Agent that generated code: DeepSeek in Kodik
- Agent that integrated code: Gemma-4-31B in Claude Code
- Date:

---

## 2. Commands to run

Adapt to the current stage.

```bash
git status
git diff --stat
```

Backend tasks:

```bash
cd backend
python -m pytest
python -m compileall app
```

Docker tasks:

```bash
docker compose config
docker compose up -d --build
docker compose ps
```

Alembic tasks:

```bash
cd backend
alembic upgrade head
alembic current
```

API smoke tests:

```bash
curl -f http://localhost:8000/health
curl -f http://localhost:8000/api/v1/health
```

---

## 3. Smoke tests

Check only what belongs to the current task.

- Backend imports successfully.
- Health endpoint returns OK.
- Docker Compose config is valid when Docker exists.
- Database migration runs when Alembic exists.
- Upload endpoint works only after upload task.
- No real external LLM call is required unless the task explicitly asks for it.

---

## 4. Manual review

Verify:

- no changes to `docs/SDD.md` except initial copy from source;
- no secrets in diff;
- no broad rewrite outside task scope;
- routes stay thin;
- storage access is behind clients/repositories;
- LLM calls, when introduced, go only through `LLMGateway`;
- all documents/chunks/facts models include or plan `access_level`;
- stubs/mocks are documented.

---

## 5. Expected git diff

The diff should contain:

- files listed in the task;
- minimal supporting files;
- tests or smoke checks when appropriate;
- updated `docs/HANDOFF.md`.

The diff should not contain:

- `.env`;
- real credentials;
- unrelated frontend/backend rewrites;
- future task implementations;
- generated cache files;
- local IDE files.

---

## 6. Commit decision

Commit only if:

- Definition of Done is met;
- checks pass or non-blocking issues are documented;
- `docs/HANDOFF.md` is updated;
- `git diff` is scoped;
- no secrets are present.

Recommended command:

```bash
git add <files>
git commit -m "TASK_XXX: short summary"
```
