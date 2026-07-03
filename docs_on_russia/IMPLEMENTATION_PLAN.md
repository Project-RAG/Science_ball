# План реализации

## Принципы

- Реализовывать одну небольшую задачу за раз.
- Одна задача должна быть проверяема и тестируема независимо.
- DeepSeek генерирует ограниченный код.
- Gemma интегрирует и валидирует.
- Коммит после каждой принятой задачи.
- Не редактировать `docs/SDD.md`.

---

## Фаза 1 — Фундамент backend

### TASK_001_backend_skeleton

Цель: создать минимальный скелет FastAPI backend.

Контекст:
- Разделы `docs/SDD.md`: backend-сервисы, API routes, структура проекта.
- `docs/AI_RULES.md`.

Файлы для создания/изменения:
- `backend/app/main.py`
- `backend/app/api/router.py`
- `backend/app/api/routes/health.py`
- `backend/app/settings.py`
- `backend/app/dependencies.py`
- `backend/tests/unit/test_health.py`
- `backend/pyproject.toml` или файл зависимостей

Не делать:
- добавлять реальные клиенты БД;
- добавлять Docker Compose;
- добавлять логику загрузки;
- реализовывать auth;
- добавлять LLM код.

Проверки:

```bash
cd backend
python -m pytest
python -m compileall app
```

Definition of Done:
- FastAPI app импортируется;
- health endpoint существует;
- тесты проходят;
- настройки загружаются без секретов.

Ожидаемое обновление handoff:
- статус скелета backend;
- изменённые файлы;
- результат валидации;
- следующая задача `TASK_002_docker_compose_and_settings`.

---

### TASK_002_docker_compose_and_settings

Цель: добавить Docker Compose и настройки окружения для MVP инфраструктуры.

Файлы:
- `docker-compose.yml`
- `.env.example`
- `.gitignore`
- `backend/Dockerfile`
- `backend/app/settings.py`
- опционально `Makefile`

Не делать:
- хардкодить секреты;
- реализовывать клиенты хранилищ;
- реализовывать миграции;
- реализовывать frontend.

Проверки:

```bash
docker compose config
```

Definition of Done:
- compose config валидируется;
- все переменные окружения сервисов используют заполнители или `.env`;
- `.env` игнорируется git.

Ожидаемое обновление handoff:
- перечисленные сервисы;
- добавленные переменные окружения;
- любые сервисы, не запущенные локально.

---

### TASK_003_storage_clients

Цель: добавить базовые фабрики клиентов хранилищ для PostgreSQL, Redis, Elasticsearch, Neo4j, MinIO.

Файлы:
- `backend/app/db/postgres.py`
- `backend/app/db/redis.py`
- `backend/app/db/elasticsearch.py`
- `backend/app/db/neo4j.py`
- `backend/app/db/minio.py`
- `backend/app/api/routes/health.py`
- тесты для конфигурации/инициализации клиентов с моками, где практично

Не делать:
- создавать SQLAlchemy модели;
- создавать Alembic миграции;
- реализовывать загрузку;
- создавать маппинги Elasticsearch;
- писать логику графа Neo4j.

Проверки:

```bash
cd backend
python -m pytest
python -m compileall app
```

Definition of Done:
- клиенты могут быть сконструированы из настроек;
- health route может показывать базовый статус приложения без необходимости запуска всех сервисов;
- секреты не логируются.

Ожидаемое обновление handoff:
- добавленные модули клиентов;
- поведение подключения;
- заглушки/моки.

---

### TASK_004_postgres_models_and_alembic

Цель: добавить базовые SQLAlchemy модели и настройку Alembic для основных транзакционных таблиц.

Файлы:
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/versions/...`
- `backend/app/models/base.py`
- `backend/app/models/document.py`
- `backend/app/models/ingestion_job.py`
- `backend/app/models/chunk.py`
- `backend/app/models/fact.py`
- `backend/app/models/audit_log.py`
- тесты/проверки миграций, если практично

Не делать:
- реализовывать upload endpoint;
- реализовывать workflow проверки фактов;
- реализовывать auth/RBAC полностью;
- реализовывать индексацию Elasticsearch.

Проверки:

```bash
cd backend
alembic upgrade head
python -m pytest
```

Definition of Done:
- миграция создаёт основные таблицы;
- таблицы document/chunk/fact содержат трассируемость и `access_level`, где требуется;
- бинарные файлы не хранятся в PostgreSQL.

Ожидаемое обновление handoff:
- ID миграции;
- созданные таблицы;
- любые компромиссы схемы.

---

### TASK_005_document_upload_minio

Цель: реализовать MVP загрузку документов в MinIO с записью метаданных в PostgreSQL.

Файлы:
- `backend/app/api/routes/documents.py`
- `backend/app/schemas/documents.py`
- `backend/app/services/ingestion/document_upload_service.py`
- `backend/app/repositories/documents.py`
- `backend/app/db/minio.py`
- тесты для сервиса/API загрузки с моками

Не делать:
- парсить документы;
- разбивать на чанки;
- запускать Celery ingestion;
- индексировать в Elasticsearch;
- писать граф Neo4j;
- вызывать LLM.

Проверки:

```bash
cd backend
python -m pytest
```

Definition of Done:
- `POST /api/v1/documents/upload` принимает разрешённые типы файлов для MVP;
- исходный файл сохранён в MinIO;
- метаданные сохранены в PostgreSQL;
- контрольная сумма записана;
- `access_level` записан;
- загрузка не раскрывает секреты.

Ожидаемое обновление handoff:
- поведение endpoint'а;
- ограничения типов файлов;
- заглушки для будущего парсинга/приёма.

---

## Фаза 2 — MVP приёма (Ingestion)

### TASK_006_ingestion_job_status

Цель: добавить использование модели ingestion job, API статуса задачи и заглушку Celery задачи.

Не парсить документы пока.

Проверки:

```bash
cd backend
python -m pytest
```

Definition of Done:
- загрузка может создавать или ссылаться на ingestion job;
- endpoint статуса задачи возвращает pending/running/succeeded/failed;
- заглушка Celery задачи подключена, но минимальна.

---

### TASK_007_text_parsers

Цель: реализовать парсеры для TXT, Markdown, PDF, DOCX для MVP.

Не разбивать на чанки/индексировать/извлекать факты пока.

Definition of Done:
- сервис парсинга возвращает текст и базовые метаданные;
- тесты используют небольшие примеры файлов.

---

### TASK_008_chunking_service

Цель: реализовать детерминированное разбиение текста на чанки с трассируемостью документ/чанк.

Definition of Done:
- чанки сохранены в PostgreSQL;
- каждый чанк имеет `document_id`, порядок/индекс, текст, опционально страницу/секцию, `access_level`.

---

## Фаза 3 — NLP MVP

### TASK_009_dictionary_entity_extraction

Цель: извлекать доменные сущности с использованием онтологических словарей.

Definition of Done:
- извлечение Material/Process/Equipment работает с алиасами;
- нет зависимости от LLM.

### TASK_010_numeric_extractor_and_units

Цель: извлекать числовые условия через regex/parser и нормализовать единицы измерения.

Definition of Done:
- температура, pH, скорость потока, давление, концентрация — примеры протестированы;
- сырые и нормализованные значения сохранены.

### TASK_011_confidence_service

Цель: реализовать MVP оценку доверия (confidence scoring).

Definition of Done:
- факты получают confidence на основе детерминированных входных данных;
- правило ограничения для LLM-only представлено для будущего использования LLM.

---

## Фаза 4 — Индексация и граф

### TASK_012_elasticsearch_mappings

Цель: создать маппинги индексов Elasticsearch для docs, chunks, entities, facts.

Definition of Done:
- маппинги содержат `access_level`;
- числовые поля и вложенные числовые условия представлены;
- размерность вектора конфигурируема.

### TASK_013_indexing_chunks_and_facts

Цель: индексировать документы/чанки/факты в Elasticsearch.

Definition of Done:
- сервис индексации записывает доступные для поиска доказательства;
- уровень доступа включён во все документы.

### TASK_014_neo4j_graph_writer

Цель: записывать базовые узлы/рёбра графа из извлечённых фактов.

Definition of Done:
- созданы ограничения;
- рёбра графа содержат метаданные факта/источника.

---

## Фаза 5 — Интеграция LLM

### TASK_015_llm_gateway_mock_and_yandex

Цель: реализовать абстракцию провайдера, mock-провайдер и оболочку Yandex провайдера.

Definition of Done:
- бизнес-код использует `LLMGateway`;
- тесты используют `MockLLMProvider`;
- секреты только из окружения.

### TASK_016_query_understanding

Цель: реализовать понимание запроса с YandexGPT через gateway и детерминированный fallback.

Definition of Done:
- вывод валидирован через Pydantic;
- fallback работает при ошибке LLM.

---

## Фаза 6 — Поиск и ответы

### TASK_017_search_api_basic

Цель: реализовать поисковый API на базе Elasticsearch с фильтрацией доступа.

Definition of Done:
- запрос применяет фильтр `access_level`;
- возвращает ранжированные чанки/доказательства.

### TASK_018_answer_synthesis_with_evidence

Цель: генерировать ответы только на основе доказательств через `LLMGateway`.

Definition of Done:
- нет доказательств — нет выдуманного ответа;
- ответ включает источники/confidence/пробелы.

---

## Фаза 7 — Верификация и frontend MVP

### TASK_019_fact_review_api

Цель: реализовать API для ожидания/подтверждения/отклонения/комментирования фактов с версионированием.

### TASK_020_frontend_document_upload

Цель: добавить экран загрузки.

### TASK_021_frontend_search_and_answer

Цель: добавить поиск и отображение ответов.

### TASK_022_frontend_graph_preview

Цель: добавить базовый просмотр графа.

---

## Фаза 8 — Полировка демо

### TASK_023_markdown_export

Цель: экспорт ответа в Markdown.

### TASK_024_demo_data_and_script

Цель: добавить примеры данных и скрипт демо.

---

## Открытые вопросы

| ID | Вопрос | Путь для MVP |
|---|---|---|
| OQ-001 | SDD содержит дублированные/искажённые фрагменты. | Использовать чистый повторяющийся смысл, не редактировать SDD. |
| OQ-002 | Точные лимиты загрузки не указаны. | Добавить настраиваемые консервативные значения по умолчанию. |
| OQ-003 | Сроки полного auth/RBAC неясны. | Сохранять `access_level` с самого начала, auth реализовать позже. |
| OQ-004 | Размерности эмбеддингов зависят от провайдера. | Сделать размерность конфигурируемой и версионировать индексы. |
