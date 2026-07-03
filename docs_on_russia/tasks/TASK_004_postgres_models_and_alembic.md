# TASK_004_postgres_models_and_alembic

## Цель

Добавить SQLAlchemy модели и настройку Alembic для основных PostgreSQL транзакционных таблиц, требуемых SDD.

Эта задача создаёт только фундамент схемы. Она не должна реализовывать загрузку или workflow приёма.

---

## Входной контекст

Прочитать перед кодированием:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- файлы предыдущих задач 001-003
- этот файл задачи

Соответствующие области SDD:

- Дизайн PostgreSQL.
- Требуемые таблицы: users, roles, user_roles, documents, document_versions, ingestion_jobs, chunks, entities, facts, fact_versions, fact_reviews, audit_log, saved_queries, notifications, exports.
- MVP может начать с основного подмножества, но должен сохранять путь расширения.
- Documents/chunks/facts требуют поля доступа/трассировки.

---

## Файлы для создания или изменения

Ожидаемые файлы:

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

Опционально если объём остаётся небольшим:

```text
backend/app/models/user.py
backend/app/models/role.py
backend/app/models/export.py
```

---

## Требуемые основные таблицы для этой задачи

Реализовать как минимум:

- `documents`
- `document_versions`, если достаточно просто, иначе задокументировать в handoff для следующей задачи схемы
- `ingestion_jobs`
- `chunks`
- `entities`, если достаточно просто
- `facts`
- `fact_versions`
- `fact_reviews`, если достаточно просто
- `audit_log`

Минимальные обязательные поля:

### documents

- `id` UUID первичный ключ
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

- `id` UUID первичный ключ
- `document_id`
- `chunk_index`
- `text`
- `language`
- `page`
- `section`
- `access_level`
- `created_at`

### facts

- `id` UUID первичный ключ
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

- `id` UUID первичный ключ
- `fact_id`
- `version`
- `payload` JSON/JSONB
- `changed_by`
- `change_reason`
- `created_at`

### audit_log

- `id` UUID первичный ключ
- `user_id`
- `action`
- `entity_type`
- `entity_id`
- `payload` JSON/JSONB
- `created_at`

---

## Явно не делать

Не делать:

- реализовывать upload endpoint документа;
- реализовывать репозитории сверх необходимого для тестов моделей;
- реализовывать парсинг файлов;
- реализовывать Celery приём;
- реализовывать индексацию Elasticsearch;
- реализовывать запись графа Neo4j;
- реализовывать API проверки фактов;
- реализовывать auth/RBAC логику сверх nullable полей пользователя или простых таблиц;
- вызывать LLM;
- изменять `docs/SDD.md`.

---

## Команды валидации

Из корня репозитория:

```bash
cd backend
alembic upgrade head
python -m pytest
python -m compileall app
```

Если нет живого PostgreSQL, Gemma может валидировать генерацию/импорт миграции и задокументировать, что полная миграция БД не была запущена.

---

## Definition of Done

- Alembic настроен против metadata приложения.
- Существуют основные SQLAlchemy модели.
- Существует начальная миграция.
- Миграция создаёт основные таблицы.
- `documents`, `chunks` и `facts` сохраняют требования трассируемости и `access_level`.
- Бинарные файлы не хранятся в PostgreSQL.
- Существующие тесты backend всё ещё проходят.
- `docs/HANDOFF.md` обновлён Gemma.

---

## Ожидаемое обновление handoff

Gemma должен обновить:

- ID ревизии миграции;
- реализованные таблицы;
- отложенные таблицы, если есть;
- результаты валидации;
- заметки о доступности БД;
- следующая задача: `TASK_005_document_upload_minio.md`;
- готовность к коммиту.
