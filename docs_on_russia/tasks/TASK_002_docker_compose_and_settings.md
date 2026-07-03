# TASK_002_docker_compose_and_settings

## Цель

Добавить Docker Compose и централизованные настройки окружения для MVP инфраструктуры без реализации логики хранилищ.

Эта задача делает проект готовым к запуску backend вместе с сервисами инфраструктуры в локальной разработке.

---

## Входной контекст

Прочитать перед кодированием:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- `docs/tasks/TASK_001_backend_skeleton.md`
- этот файл задачи

Соответствующие области SDD:

- Сервисы Docker Compose: backend, worker, postgres, elasticsearch, neo4j, redis, minio.
- Безопасность: секреты только в `.env`.
- Переменные окружения YandexGPT только для backend/worker.
- Развёртывание MVP на одной машине через Docker Compose.

---

## Файлы для создания или изменения

Ожидаемые файлы:

```text
docker-compose.yml
.env.example
.gitignore
Makefile
backend/Dockerfile
backend/app/settings.py
```

Опционально если нужно:

```text
backend/.dockerignore
```

---

## Требования

Добавить сервисы Docker Compose для MVP инфраструктуры:

- `backend`
- `worker` как заполнитель/peer выполнения, если практично
- `postgres`
- `elasticsearch`
- `neo4j`
- `redis`
- `minio`

Frontend не требуется в этой задаче.

Настройки должны включать переменные окружения для:

- имя приложения/окружение/debug;
- хост/порт backend, если нужно;
- PostgreSQL;
- Redis;
- Elasticsearch;
- Neo4j;
- MinIO;
- LLM провайдер;
- заполнители YandexGPT;
- заполнители локального LLM fallback.

`.env.example` должен содержать только заполнители.

`.gitignore` должен игнорировать:

```text
.env
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
*.pyc
```

Правила Docker:

- никаких реальных секретов;
- использовать подстановку переменных из `.env`;
- не встраивать секреты в Docker образ;
- backend и worker получают LLM env vars только как переменные окружения;
- healthchecks приветствуются, но должны оставаться практичными.

---

## Явно не делать

Не делать:

- реализовывать модули клиентов хранилищ;
- добавлять модели БД;
- добавлять Alembic миграции;
- реализовывать загрузку;
- реализовывать задачи приёма;
- реализовывать маппинги Elasticsearch;
- реализовывать ограничения Neo4j;
- реализовывать LLMGateway;
- добавлять frontend сервис, если это не необходимо как заполнитель;
- коммитить `.env`;
- помещать реальный Yandex API ключ где-либо;
- изменять `docs/SDD.md`.

---

## Команды валидации

Из корня репозитория:

```bash
docker compose config
```

Если Docker доступен и зависимостей достаточно:

```bash
docker compose up -d --build postgres redis minio elasticsearch neo4j
```

Валидация backend из предыдущей задачи должна всё ещё проходить:

```bash
cd backend
python -m pytest
```

---

## Definition of Done

- `docker-compose.yml` парсится командой `docker compose config`.
- `.env.example` содержит все необходимые переменные только с заполнителями.
- `.env` игнорируется git.
- Backend настройки могут читать compose/env переменные.
- Тесты скелета backend всё ещё проходят.
- Нет преждевременно реализованной бизнес-логики хранилищ.
- Нет секретов.
- `docs/HANDOFF.md` обновлён Gemma.

---

## Ожидаемое обновление handoff

Gemma должен обновить:

- добавленные сервисы;
- добавленные настройки;
- результаты команд валидации;
- заметки о доступности Docker;
- любые проблемы запуска сервисов;
- следующая задача: `TASK_003_storage_clients.md`;
- готовность к коммиту.
