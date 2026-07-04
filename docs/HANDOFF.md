# HANDOFF

## Текущий статус

- Текущая задача: `TASK_019_fact_review_api`
- Статус: завершена
- Последнее обновление: Gemma (Интегратор)
- Дата обновления: 2026-07-04

---

## Выполненные задачи

| Задача | Статус | Примечания |
|---|---|---|
| TASK_017_search_api_basic | завершена | Базовый API поиска реализован |
| TASK_018_answer_synthesis_with_evidence | завершена | Синтез ответов на основе evidence реализован |
| TASK_019_fact_review_api | завершена | API верификации и редактирования фактов реализован |

---

## Текущее состояние репозитория

### Реализовано
- **Fact Review Workflow**: Реализован полный цикл человеческой проверки извлеченных фактов.
- **Audit Trail**: Создан `AuditLogRepository` для записи всех действий с фактами (верификация, отклонение, комментирование, редактирование).
- **Versioning**: Реализована система версионирования через `FactVersion`. При редактировании существующего факта его текущее состояние сохраняется в историю перед обновлением.
- **Review API**:
    - `GET /api/v1/facts/pending-review`: Список фактов со статусом `machine_extracted` с фильтрацией по документу и confidence.
    - `POST /api/v1/facts/{id}/verify`: Перевод в статус `expert_verified`.
    - `POST /api/v1/facts/{id}/reject`: Перевод в статус `rejected` с обязательной причиной.
    - `POST /api/v1/facts/{id}/comment`: Добавление комментария в аудит-лог без смены статуса.
    - `PATCH /api/v1/facts/{id}`: Редактирование значений факта + перевод в `expert_verified`.
- **Service Layer**: `FactReviewService` инкапсулирует логику переходов состояний и запись аудита.

### Не реализовано
- Интеграция с JWT-авторизацией (в роутах используются заглушки для `user_id`).
- Продвинутый расчет confidence score при экспертной правке.

---

## Изменённые файлы в последней задаче

```text
backend/app/repositories/audit_logs.py (New)
backend/app/repositories/facts.py (Updated)
backend/app/schemas/facts.py (New)
backend/app/services/review/fact_review_service.py (New)
backend/app/api/routes/facts.py (New)
backend/app/api/router.py (Updated)
backend/tests/unit/test_fact_review_service.py (New)
```

---

## Запущенные команды валидации

```bash
cd backend && python -m pytest tests/unit/test_fact_review_service.py
cd backend && python -m compileall app
```

Результат:
```text
pytest: 3 passed
compileall: Успешно (без ошибок)
```

---

## Заглушки и моки

| Область | Заглушка/мок | Причина | Задача удаления |
|---|---|---|---|
| Auth | `user_id: UUID \| None = None` в роутах | Интеграция с JWT отложена | TASK_XXX (Auth) |
| LLM | `MockLLMProvider` | Для тестов и локальной разработки без API ключа | По умолчанию в настройках |

---

## Известные проблемы

| ID | Проблема | Серьёзность | Обход | Целевая задача |
|---|---|---|---|---|
| REV-001 | Отсутствует проверка прав доступа (RBAC) на уровне API для ревьюеров | Средняя | Ожидается внедрение системы ролей | TASK_XXX (Auth/RBAC) |

---

## Следующая задача

Рекомендуемая следующая задача:

```text
TASK_020_frontend_document_upload.md
```

Прочитать перед началом:
- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- `docs/tasks/TASK_020_frontend_document_upload.md`

Что следующая задача должна переиспользовать из этой:
- API эндпоинты загрузки документов (уже существующие), которые будут связаны с фронтендом.
- Понимание структуры `documents` и `ingestion_jobs`, так как загрузка файлов запускает весь pipeline, который в итоге создает факты для ревью.

---

## Готовность к коммиту

- Готов к коммиту: да
- Причина: TASK_019 полностью реализована, покрыта unit-тестами и проверена на отсутствие ошибок компиляции.
