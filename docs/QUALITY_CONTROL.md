# Quality Control Rules

## 1. Preventing DeepSeek scope drift

Give DeepSeek exactly one task file.

Prompt must say:
- implement only this task;
- do not implement future tasks;
- do not rewrite architecture;
- do not edit `docs/SDD.md`;
- list changed files;
- list stubs and checks.

Reject DeepSeek output if it:
- creates large unrelated modules;
- implements multiple stages;
- hardcodes secrets;
- calls YandexGPT directly outside `LLMGateway`;
- puts storage logic into routes;
- changes SDD or orchestration docs without request.

---

## 2. Preventing Gemma from rewriting the project

Gemma prompt must say:
- integrate, do not rewrite;
- preserve existing architecture;
- fix only what is needed for the current task;
- record broader fixes in handoff;
- do not delete previous work unless necessary and documented.

Reject Gemma output if it:
- replaces directory structure without reason;
- changes technology choices from SDD;
- merges future tasks into current task;
- removes tests instead of fixing them;
- hides failing checks.

---

## 3. Handling non-working generated code

If DeepSeek code does not run:

1. Gemma identifies the smallest failing surface.
2. Gemma fixes imports/config/dependencies first.
3. Gemma avoids redesign unless the generated code contradicts SDD.
4. If still failing, Gemma documents the issue in `Known Issues`.
5. The task is not committed unless the failure is non-blocking and explicitly documented.

---

## 4. Stubs and mocks policy

Stubs/mocks are allowed only when:
- the real integration is scheduled for a later task;
- the stub has a clear interface compatible with planned implementation;
- the stub is documented in `docs/HANDOFF.md`.

Each stub entry must include:
- file/module;
- behavior;
- reason;
- task where it should be replaced.

Never hide a stub as production-ready behavior.

---

## 5. Known issues policy

Known issues must be tracked in `docs/HANDOFF.md`.

Each issue should include:
- id;
- short description;
- severity;
- workaround;
- target task or decision point.

Severity levels:
- blocker — cannot continue or commit;
- high — task works but next stage is risky;
- medium — acceptable for MVP if tracked;
- low — cleanup/documentation.

---

## 6. Secret scanning checklist

Before commit, check:

```bash
git diff
```

Look for:
- `YANDEX_API_KEY` with real value;
- passwords;
- tokens;
- private keys;
- Authorization headers;
- `.env` added to git.

`.env.example` must contain placeholders only.

---

## 7. Architecture checklist

For every task, verify:

- FastAPI routes are thin.
- Business logic is in services.
- PostgreSQL persistence is in models/repositories.
- Elasticsearch access is in a client/service.
- Neo4j access is in a graph client/service.
- MinIO access is in object storage client.
- LLM access is through `LLMGateway` only.
- Search always considers `access_level` once search is implemented.
- Facts trace to document/chunk once facts are implemented.
