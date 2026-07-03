# HANDOFF

## Текущий статус

- Текущая задача: `TASK_004_postgres_models_and_alembic`
- Статус: завершена
- Последнее обновление: Gemma (Интегратор)
- Последнее обновление: 2026-07-03

---

## Выполненные задачи

| Задача | Статус | Коммит | Примечания |
|---|---|---|---|
| TASK_000_project_orchestration_docs | завершена | TBD | Созданы документы оркестрации |
| TASK_001_backend_skeleton | завершена | TBD | Скелет FastAPI реализован и проверен |
| TASK_002_docker_compose_and_settings | завершена | TBD | Инфраструктура в Docker, настройки централизованы |
| TASK_003_storage_clients | завершена | TBD | Фабрики клиентов хранилищ реализованы |
| TASK_004_postgres_models_and_alembic | завершена | TBD | SQLAlchemy модели и Alembic миграции настроены |

---

## Текущее состояние репозитория

### Реализовано
- Документация оркестрации и список задач.
- SDD скопирован в `docs/SDD.md`.
- Минимальный скелет FastAPI backend (фабрика приложения, health endpoints).
- Полная MVP инфраструктура в `docker-compose.yml` (Postgres, Redis, ES, Neo4j, MinIO).
- Backend Dockerfile с multistage сборкой и non-root пользователем.
- Централизованная модель настроек, читающая переменные окружения.
- Фабрики клиентов хранилищ для всех backend'ов (ленивая загрузка).
- SQLAlchemy 2.0 Core модели для MVP:
    - `documents` (access_level, ссылки MinIO)
    - `chunks` (трассируемость, access_level)
    - `entities` (извлечённые сущности, алиасы)
    - `facts` и `fact_versions` (единицы знаний, трассируемость, confidence)
    - `ingestion_jobs` (отслеживание pipeline)
    - `audit_log` (неизменяемый журнал аудита)
- Настроен Alembic migration framework с начальной ревизией.

### Не реализовано
- Логика загрузки документов и интеграция MinIO.
- Реализация pipeline приёма (ingestion).
- Бизнес-логика NLP/поиска/графа/LLM.
- Frontend.

---

## Изменённые файлы в последней задаче

```text
backend/pyproject.toml
backend/alembic.ini
backend/alembic/env.py
backend/alembic/script.py.mako
backend/alembic/versions/26fb8bfa9ca6_initial_core_tables.py
backend/app/models/__init__.py
backend/app/models/base.py
backend/app/models/document.py
backend/app/models/chunk.py
backend/app/models/entity.py
backend/app/models/fact.py
backend/app/models/ingestion_job.py
backend/app/models/audit_log.py
backend/tests/unit/test_models.py
```

---

## Запущенные команды валидации

```bash
cd backend && python -m pytest
cd backend && python -m compileall app
```

Результат:
```text
pytest: 63 passed (включая тесты моделей и миграций)
compileall: Успешно (без ошибок)
```

---

## Схема БД и миграции

### Ревизия миграции
- ID: `26fb8bfa9ca6`
- Название: `initial_core_tables`

### Созданные таблицы
- `documents`: Метаданные, контрольные суммы и уровни доступа.
- `chunks`: Сегменты документов с трассируемостью.
- `entities`: Извлечённые именованные сущности.
- `facts`: Единицы знаний с confidence и трассировкой источника.
- `fact_versions`: Версионирование фактов через JSONB payload.
- `ingestion_jobs`: Отслеживание состояния pipeline приёма.
- `audit_log`: Неизменяемый журнал действий пользователя.

---

## Заглушки и моки

| Область | Заглушка/мок | Причина | Задача удаления |
|---|---|---|---|
| Зависимости | `backend/app/dependencies.py` пуст | Фаза скелета; реальные зависимости в следующих задачах | TASK_005+ |
| Worker | сервис `worker` в compose | Заполнитель для Celery; задач пока нет | TASK_005+ |
| RBAC | поля user_id / created_by | Nullable UUID без внешних ключей (таблица Users отложена) | Задача: реализация Auth/RBAC |

---

## Известные проблемы

| ID | Проблема | Серьёзность | Обход | Целевая задача |
|---|---|---|---|---|
| НЕТ | - | - | - | - |

---

## Открытые вопросы

| ID | Вопрос | Практический путь для MVP | Решение |
|---|---|---|---|
| OQ-001 | SDD содержит дублированные/искажённые фрагменты. | Считать чистыми маркированные списки и блоки кода. Не редактировать SDD. | Ожидает |
| OQ-002 | Точные лимиты размера загрузки не указаны. | Использовать консервативные настраиваемые значения по умолчанию. | Ожидает |
| OQ-003 | Глубина Auth/RBAC для раннего MVP не указана. | Начать с полей `access_level`, позже добавить реальный auth/RBAC. | Ожидает |

---

## Заметки по окружению

Необходимые локальные секреты должны находиться только в `.env`.

Никогда не коммитить:
- `.env`;
- реальный Yandex API ключ;
- реальные пароли БД;
- реальные учётные данные MinIO/Neo4j.

---

## Следующая задача

Рекомендуемая следующая задача:

```text
TASK_005_document_upload_minio.md
```

Прочитать перед началом:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- `docs/tasks/TASK_005_document_upload_minio.md`

---

## Готовность к коммиту

- Готов к коммиту: да
- Причина: TASK_004 полностью реализована и проверена. Модели строго соответствуют требованиям SDD (трассируемость, уровни доступа). Alembic настроен, начальная миграция присутствует. Бизнес-логика не просочилась.
- Требуется перед коммитом: ничего
