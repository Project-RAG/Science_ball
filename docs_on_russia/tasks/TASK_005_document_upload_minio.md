# TASK_005_document_upload_minio

## Цель

Реализовать MVP endpoint загрузки документов, который сохраняет исходный файл в MinIO и записывает метаданные документа в PostgreSQL.

Эта задача реализует только загрузку. Парсинг, разбиение на чанки, Celery приём, индексация Elasticsearch, запись графа Neo4j и LLM вызовы остаются будущими задачами.

---

## Входной контекст

Прочитать перед кодированием:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- файлы предыдущих задач 001-004
- этот файл задачи

Соответствующие области SDD:

- API документов: `POST /api/v1/documents/upload`.
- Pipeline приёма начинается с загрузки файла → сохранения оригинала в MinIO → создания метаданных документа в PostgreSQL.
- Таблица PostgreSQL `documents`.
- MinIO хранит исходные документы.
- Все документы должны иметь `access_level`.
- Секреты не должны быть раскрыты.

---

## Файлы для создания или изменения

Ожидаемые файлы:

```text
backend/app/api/router.py
backend/app/api/routes/documents.py
backend/app/schemas/__init__.py
backend/app/schemas/documents.py
backend/app/services/__init__.py
backend/app/services/ingestion/__init__.py
backend/app/services/ingestion/document_upload_service.py
backend/app/repositories/__init__.py
backend/app/repositories/documents.py
backend/app/db/minio.py
backend/app/models/document.py
backend/tests/unit/test_document_upload_service.py
```

Опционально если нужно:

```text
backend/tests/unit/test_documents_api.py
```

---

## Требования

Реализовать endpoint:

```text
POST /api/v1/documents/upload
```

Endpoint должен принимать multipart form upload с метаданными, такими как:

- file;
- title;
- source_type;
- access_level;
- language опционально;
- year опционально.

MVP разрешённые расширения файлов:

- `.pdf`
- `.docx`
- `.txt`
- `.md`
- `.csv`
- `.xlsx`

Сервис загрузки должен:

1. валидировать разрешённое расширение файла/имя на уровне MVP;
2. вычислить контрольную сумму;
3. сгенерировать ключ объекта MinIO;
4. сохранить исходный файл в MinIO;
5. создать строку метаданных документа в PostgreSQL через репозиторий;
6. вернуть ID документа и метаданные;
7. не парсить содержимое пока.

Репозиторий должен:

- использовать SQLAlchemy сессию;
- создавать строку документа;
- не хранить байты файла в PostgreSQL.

Helper клиента MinIO должен:

- использовать настройки;
- избегать логирования секретов;
- предоставлять upload helper, если уместно.

---

## Явно не делать

Не делать:

- парсить содержимое файлов;
- создавать чанки;
- создавать Celery задачу приёма, если крошечный заполнитель уже существует и не требуется;
- индексировать в Elasticsearch;
- писать в Neo4j;
- вызывать YandexGPT или любую LLM;
- реализовывать frontend UI загрузки;
- реализовывать полный auth/RBAC;
- реализовывать сканирование вирусов/OCR;
- изменять `docs/SDD.md`.

---

## Команды валидации

Из корня репозитория:

```bash
cd backend
python -m pytest
python -m compileall app
```

Если Docker сервисы доступны:

```bash
docker compose up -d postgres minio
cd backend
alembic upgrade head
python -m pytest
```

Опциональный API smoke после запуска приложения:

```bash
curl -f http://localhost:8000/health
```

---

## Definition of Done

- `POST /api/v1/documents/upload` зарегистрирован.
- Сервис загрузки сохраняет исходный файл в MinIO через абстракцию клиента.
- Метаданные документа сохранены в PostgreSQL через репозиторий.
- `checksum`, `minio_bucket`, `minio_object_key`, `access_level` записаны.
- Тесты покрывают поведение сервиса с моками/заглушками.
- Байты файла не хранятся в PostgreSQL.
- Нет преждевременно реализованной работы по парсингу/разбиению/индексации/графу/LLM.
- Нет раскрытых секретов.
- `docs/HANDOFF.md` обновлён Gemma.
