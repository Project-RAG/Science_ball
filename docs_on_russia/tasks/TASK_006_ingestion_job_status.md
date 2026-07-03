# TASK_006_ingestion_job_status

## Цель

Добавить создание/отслеживание статуса задачи приёма (ingestion job) и минимальную границу Celery задачи для обработки документов.

---

## Входной контекст

Прочитать перед кодированием:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- файлы предыдущих задач по применимости
- этот файл задачи

Соответствующий контекст:

- файлы предыдущих задач 001-005
- SDD pipeline приёма, Redis/Celery, PostgreSQL ingestion jobs

---

## Файлы для создания или изменения

Ожидаемые файлы:

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

Добавлять минимальные вспомогательные файлы только когда требуется импортами/тестами.

---

## Требования

- Создавать или переиспользовать строку ingestion job при загрузке документа или отправке на приём.
- Предоставить `GET /api/v1/ingestion/jobs/{job_id}`.
- Предоставить `POST /api/v1/ingestion/jobs/{job_id}/enqueue` или эквивалентный минимальный триггер.
- Определить статусы задачи: pending, queued, running, succeeded, failed.
- Подключить Celery app и задачу-заполнитель без парсинга документов пока.
- Держать routes тонкими; использовать слои service/repository.

---

## Явно не делать

Не делать:

- парсить документы
- разбивать текст на чанки
- индексировать Elasticsearch
- писать граф Neo4j
- вызывать LLM
- реализовывать frontend
- изменять `docs/SDD.md`
- коммитить реальные секреты или приватные данные

---

## Команды валидации

Из корня репозитория, адаптировать под текущий этап:

```bash
cd backend
python -m pytest
python -m compileall app
```

Если изменены frontend файлы:

```bash
cd frontend
npm install
npm run build
```

Если требуются Docker сервисы и они доступны:

```bash
docker compose up -d
```

---

## Definition of Done

- API статуса задачи возвращает текущее состояние.
- Поток загрузки может ссылаться или создавать ingestion job.
- Граница Celery задачи существует и может быть импортирована.
- Тесты покрывают поведение job service/status с моками/заглушками.
- Нет преждевременно реализованной работы по парсингу/разбиению/индексации/LLM.
- `docs/HANDOFF.md` обновлён Claude Code с Gemma-4-31B.

---

## Ожидаемое обновление handoff

Claude Code с Gemma-4-31B должен обновить `docs/HANDOFF.md`:

- статус задачи;
- изменённые файлы;
- команды валидации и результаты;
- заметки по выполнению;
- заглушки/заполнители;
- известные проблемы;
- следующая задача: `TASK_007_text_parsers.md`;
- готовность к коммиту.
