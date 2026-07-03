# AI Rules for R&D Knowledge Map

## 1. Purpose

This document defines rules for AI-assisted implementation of the R&D Knowledge Map project.

Primary sources of truth:
- `docs/SDD.md` — architecture and product requirements. Do not edit it during implementation tasks.
- `docs/IMPLEMENTATION_PLAN.md` — phased execution plan.
- `docs/HANDOFF.md` — current implementation state.
- `docs/tasks/TASK_XXX_...md` — current scoped task.

The project must be implemented iteratively, in small verifiable tasks. No AI agent may generate or rewrite the whole project at once.

---

## 2. Agent roles

### 2.1 DeepSeek in Kodik

DeepSeek is the code generator for one small task at a time.

DeepSeek must:
- read only the relevant project docs and current task;
- implement the minimum code required by the current task;
- keep business logic out of API routes;
- place external storage access behind clients/repositories;
- use stubs/mocks only when explicitly allowed by the task;
- list all created/changed files at the end;
- list commands that should validate the result.

DeepSeek must not:
- implement future tasks;
- rewrite architecture from `docs/SDD.md`;
- edit `docs/SDD.md`;
- commit changes;
- store secrets in source code, frontend, tests, docs, Docker images, or git;
- call YandexGPT directly from routes or business services;
- put PostgreSQL/Elasticsearch/Neo4j/MinIO/Redis logic directly into routes.

### 2.2 Gemma-4-31B in Claude Code

Gemma is the integrator. It takes DeepSeek output and makes it runnable in the real repository.

Gemma must:
- verify that changes match the current task scope;
- fix imports, dependencies, config, Docker, Alembic, tests, and formatting;
- preserve the SDD architecture;
- run focused checks;
- update `docs/HANDOFF.md` after every task;
- record stubs, mocks, known issues, and next step;
- keep changes minimal.

Gemma must not:
- rewrite the project from scratch;
- replace the architecture or storage technologies;
- edit `docs/SDD.md`;
- implement multiple tasks in one pass;
- remove previous task work unless it is broken and the fix is documented;
- commit unless explicitly instructed by the user.

---

## 3. Scope control

Each task is limited to the files and behaviors listed in its task file.

Allowed out-of-scope changes:
- import fixes;
- dependency list updates;
- minimal config wiring;
- tests needed to validate the task;
- `docs/HANDOFF.md` update by Gemma.

If an agent needs broader changes, it must record:
- why the change was necessary;
- which files were affected;
- whether this creates a new known issue or open question.

Forbidden scope expansion:
- implementing future APIs early;
- adding frontend during backend-only tasks;
- adding LLM provider code before the LLM task;
- adding advanced NLP before dictionary/regex MVP tasks;
- adding monitoring stack before MVP requires it.

---

## 4. Secrets and security

Secrets must exist only in local `.env` and runtime environment variables.

Never store these in git:
- `YANDEX_API_KEY`;
- real `YANDEX_FOLDER_ID` if private;
- PostgreSQL passwords;
- Neo4j passwords;
- MinIO access/secret keys;
- JWT secrets;
- cloud credentials;
- private keys;
- tokens.

`.env.example` may contain only placeholders such as `change_me`, never real values.

Frontend must never receive or reference Yandex API keys. All LLM calls go through backend-only `LLMGateway`.

Logs must not include:
- API keys;
- authorization headers;
- raw secrets;
- full prompts containing confidential/restricted document text.

For restricted documents, send only extracted facts/evidence to LLM, not full raw document text.

---

## 5. Runnable result requirements

Every task should leave the repository in the best possible runnable state.

Minimum expectations:
- app imports successfully;
- basic health endpoint works after backend skeleton task;
- Docker Compose config validates once Docker is introduced;
- tests for implemented logic pass;
- migrations are generated and runnable once Alembic is introduced;
- failed external services degrade clearly if the task allows stubs.

If a task cannot be fully runnable yet, this must be documented in `docs/HANDOFF.md` under `Known Issues` and `Stubs/Mocks`.

---

## 6. Docker rules

Docker Compose for MVP must include, when introduced:
- backend;
- worker;
- postgres;
- elasticsearch;
- neo4j;
- redis;
- minio.

Optional services are postponed unless a task explicitly asks for them:
- frontend;
- ollama;
- prometheus;
- grafana;
- kibana.

Docker rules:
- do not bake secrets into images;
- pass secrets via environment variables from `.env`;
- keep `.env.example` safe;
- use healthchecks where practical;
- backend and worker should share the same settings model;
- Docker changes must be validated with `docker compose config` when Docker is available.

---

## 7. Environment and settings rules

Settings must be centralized in backend configuration, preferably `backend/app/settings.py`.

Required config groups over time:
- app settings;
- PostgreSQL URL;
- Redis URL;
- Elasticsearch URL;
- Neo4j URI and credentials;
- MinIO endpoint and credentials;
- LLM provider settings;
- YandexGPT settings;
- local LLM fallback settings.

Defaults may be development-friendly, but secrets must remain placeholders.

---

## 8. Repository and layering rules

Routes should be thin.

Recommended backend layering:
- `api/routes/*` — HTTP boundary only;
- `schemas/*` — request/response DTOs;
- `services/*` — business workflows;
- `repositories/*` — transactional database operations;
- `db/*` — external clients/session factories;
- `models/*` — SQLAlchemy models;
- `workers/*` — Celery tasks.

External systems must not be accessed directly from routes:
- PostgreSQL access goes through session/repositories;
- Elasticsearch access goes through a client/service;
- Neo4j access goes through a graph client/service;
- MinIO access goes through an object storage client;
- Redis/Celery access goes through worker/config abstractions;
- LLM access goes through `LLMGateway`.

---

## 9. PostgreSQL rules

PostgreSQL is the transactional source of truth for:
- users and roles;
- documents;
- ingestion jobs;
- chunks metadata;
- facts;
- fact versions;
- reviews;
- audit log.

Rules:
- use SQLAlchemy models;
- use Alembic migrations;
- do not store original files in PostgreSQL;
- document rows must include `access_level`;
- facts must include `source_document_id` and preferably `source_chunk_id`;
- fact changes must create versions in `fact_versions` once fact editing is implemented;
- do not delete history silently.

---

## 10. Elasticsearch rules

Elasticsearch is the primary search layer for:
- full-text search;
- vector search;
- numeric filters;
- evidence retrieval.

Rules:
- all searchable documents/chunks/facts must include `access_level`;
- every search query must apply access filtering;
- mappings must use suitable types: `keyword`, `text`, `dense_vector`, `float`, `integer`, `date`, `nested`;
- do not mix embeddings of different dimensions in one index;
- if embedding dimensions change, create a new index version;
- do not replace Elasticsearch with PostgreSQL search for MVP search features.

---

## 11. Neo4j rules

Neo4j is used for graph traversal and visualization.

Rules:
- do not replace Neo4j with Elasticsearch or PostgreSQL graph emulation;
- use constraints for stable node ids;
- relationships written from facts must contain traceability metadata where available:
  - `fact_id`;
  - `source_document_id`;
  - `confidence`;
  - `verification_status`;
  - timestamps.

---

## 12. MinIO rules

MinIO stores:
- original uploaded documents;
- parsed artifacts;
- exports.

Rules:
- do not store original binary documents in PostgreSQL;
- object keys must be deterministic enough to avoid collisions;
- document metadata in PostgreSQL must point to MinIO bucket/object key;
- upload APIs must validate file type and size when implemented;
- local development may auto-create required buckets.

---

## 13. Redis and Celery rules

Redis is used for queues, cache, and job status support.

Celery is used for background tasks.

Rules:
- ingestion should become asynchronous after basic upload is working;
- routes should enqueue tasks instead of doing long processing inline;
- task status must be visible through ingestion job endpoints;
- failed jobs must preserve error information without leaking secrets.

---

## 14. LLMGateway rules

All LLM access must go through:

```text
backend/app/services/llm/llm_gateway.py
```

Provider structure:

```text
LLMProvider
  YandexLLMProvider
  LocalLLMProvider
  MockLLMProvider
```

Rules:
- business logic must not call Yandex API directly;
- routes must not call Yandex API directly;
- tests must use `MockLLMProvider`;
- YandexGPT is not a source of truth;
- LLM must answer only from evidence;
- query understanding output must be validated with Pydantic;
- if YandexGPT fails, use deterministic fallback;
- do not log API keys or authorization headers.

---

## 15. Numeric extraction rules

Numbers must be extracted deterministically with regex/parser logic.

Rules:
- do not rely on LLM as the only source for exact numeric values;
- normalize units;
- preserve raw text span when possible;
- numeric facts must trace back to `document_id` and `chunk_id` when available;
- LLM-extracted-only facts cannot receive confidence above `0.65` without verification.

---

## 16. Testing rules

Each task should add or update focused tests when possible.

Required test areas over time:
- health endpoint;
- settings loading;
- storage clients initialization with mocks;
- SQLAlchemy models and Alembic migration sanity;
- document upload with mocked MinIO;
- parsers;
- chunking;
- numeric extraction;
- unit normalization;
- query understanding fallback;
- LLMGateway with mock provider;
- access filtering in search queries.

Do not use real YandexGPT in tests.

---

## 17. Handoff rules

Gemma must update `docs/HANDOFF.md` after every task with:
- task id and title;
- status;
- changed files;
- validation commands and results;
- stubs/mocks;
- known issues;
- open questions;
- next task recommendation;
- whether commit is safe.

---

## 18. Git rules

One task should generally produce one commit.

Commit only when:
- task Definition of Done is satisfied;
- checks pass or acceptable limitations are documented;
- `docs/HANDOFF.md` is updated;
- diff contains no secrets;
- diff contains no broad unrelated rewrite.

Recommended commit message:

```text
TASK_XXX: short imperative summary
```
