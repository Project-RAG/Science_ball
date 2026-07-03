# TASK_001_backend_skeleton

## Цель

Создать минимальный скелет FastAPI backend, соответствующий структуре проекта SDD и импортируемый/тестируемый локально.

Эта задача устанавливает только границу backend-приложения. Не должна реализовывать хранилища, приём, auth, поиск, LLM или frontend.

---

## Входной контекст

Прочитать перед кодированием:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- этот файл задачи

Соответствующие области SDD:

- Стек backend: Python 3.11+, FastAPI, SQLAlchemy, Alembic, Pydantic, Celery, Redis.
- Список routes сервиса API.
- Рекомендуемая структура проекта.
- Инструкция держать бизнес-логику вне routes.

---

## Файлы для создания или изменения

Ожидаемые файлы:

```text
backend/
  app/
    __init__.py
    main.py
    settings.py
    dependencies.py
    api/
      __init__.py
      router.py
      routes/
        __init__.py
        health.py
  tests/
    __init__.py
    unit/
      __init__.py
      test_health.py
  pyproject.toml
```

Опционально если нужно:

```text
backend/README.md
```

---

## Требования

Реализовать:

- Фабрику FastAPI приложения или экземпляр приложения в `backend/app/main.py`.
- API router в `backend/app/api/router.py`.
- Health route в `backend/app/api/routes/health.py`.
- Модель настроек в `backend/app/settings.py`.
- Модуль-заполнитель зависимостей в `backend/app/dependencies.py`.
- Базовые тесты для health endpoint.

Health endpoints должны включать как минимум один стабильный endpoint:

```text
GET /health
```

Также рекомендуется предоставить версионированный API health:

```text
GET /api/v1/health
```

Ответ может быть простым:

```json
{
  "status": "ok",
  "service": "rd-knowledge-map-backend"
}
```

---

## Явно не делать

Не делать:

- добавлять Docker Compose;
- добавлять клиенты БД;
- добавлять SQLAlchemy модели;
- добавлять Alembic;
- добавлять MinIO загрузку;
- добавлять Celery worker;
- добавлять интеграцию Redis;
- добавлять интеграцию Elasticsearch;
- добавлять интеграцию Neo4j;
- добавлять auth/RBAC;
- добавлять LLMGateway;
- добавлять frontend;
- изменять `docs/SDD.md`.

---

## Команды валидации

Из корня репозитория:

```bash
cd backend
python -m pytest
python -m compileall app
```

Если зависимости ещё не установлены, задокументируйте использованную команду установки, например:

```bash
cd backend
python -m pip install -e .[dev]
python -m pytest
```

---

## Definition of Done

- Пакет backend импортируется успешно.
- FastAPI приложение запускается/импортируется без внешних сервисов.
- Тест `GET /health` проходит.
- Настройки загружаются без необходимости в секретах.
- Нет преждевременно реализованной логики хранилищ/LLM/бизнес-логики.
- Нет реальных секретов.
- `docs/HANDOFF.md` обновлён Gemma.

---

## Ожидаемое обновление handoff

Gemma должен обновить `docs/HANDOFF.md`:

- статус задачи;
- изменённые файлы;
- команды валидации и результаты;
- заметки по установке зависимостей;
- любые заглушки/заполнители;
- следующая задача: `TASK_002_docker_compose_and_settings.md`;
- готовность к коммиту.

---

## Промпт для DeepSeek в Kodik

```markdown
Ты работаешь в Kodik над проектом R&D Knowledge Map.

Текущая задача: `docs/tasks/TASK_001_backend_skeleton.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- `docs/tasks/TASK_001_backend_skeleton.md`

Сгенерируй минимальный FastAPI backend skeleton строго по текущей задаче.

Разрешено создавать/изменять только backend skeleton files, перечисленные в task.

Запрещено:
- добавлять Docker Compose;
- добавлять реальные storage clients;
- добавлять SQLAlchemy models/Alembic;
- добавлять upload/ingestion/search/LLM/frontend;
- менять `docs/SDD.md`;
- хранить секреты.

Требования:
- FastAPI app должен импортироваться без внешних сервисов;
- должен быть health endpoint;
- должны быть минимальные тесты health endpoint;
- routes должны быть тонкими;
- settings должны загружаться без реальных секретов.

В конце выдай:
1. список созданных/измененных файлов;
2. команды проверки;
3. известные stubs/placeholders;
4. что должен проверить Gemma-интегратор.
```

---

## Промпт для Gemma-4-31B в Claude Code

```markdown
Ты интегратор проекта R&D Knowledge Map.

Интегрируй результат DeepSeek по задаче `docs/tasks/TASK_001_backend_skeleton.md`.

Прочитай:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- текущий git diff

Твоя задача:
- проверить, что изменения строго соответствуют TASK_001;
- исправить импорты, зависимости, структуру пакетов, тесты;
- не добавлять Docker/storage/models/upload/search/LLM/frontend;
- не переписывать архитектуру;
- не менять `docs/SDD.md`;
- запустить проверки;
- обновить `docs/HANDOFF.md`.

Запусти по возможности:

```bash
cd backend
python -m pytest
python -m compileall app
```

Если зависимостей не хватает, добавь минимальную корректную dependency-конфигурацию и задокументируй команду установки.

В `docs/HANDOFF.md` запиши:
- changed files;
- validation results;
- stubs/placeholders;
- known issues;
- next task `TASK_002_docker_compose_and_settings.md`;
- можно ли делать commit.
