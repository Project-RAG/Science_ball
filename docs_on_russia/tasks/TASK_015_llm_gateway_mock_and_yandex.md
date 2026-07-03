# TASK_015_llm_gateway_mock_and_yandex

## Цель

Реализовать backend-only LLMGateway с mock-провайдером и адаптером YandexGPT провайдера.

---

## Входной контекст

Прочитать перед кодированием:

- `docs/SDD.md`
- `docs/AI_RULES.md`
- `docs/HANDOFF.md`
- файлы предыдущих задач по применимости
- этот файл задачи

Соответствующий контекст:

- файлы предыдущих задач 001-014
- SDD YandexGPT backend-only gateway и правила секретов

---

## Файлы для создания или изменения

Ожидаемые файлы:

- `backend/app/llm/__init__.py`
- `backend/app/llm/gateway.py`
- `backend/app/llm/providers.py`
- `backend/app/llm/mock_provider.py`
- `backend/app/llm/yandex_provider.py`
- `backend/app/schemas/llm.py`
- `backend/tests/unit/test_llm_gateway.py`

Добавлять минимальные вспомогательные файлы только когда требуется импортами/тестами.

---

## Требования

- Определить интерфейс провайдера и фасад LLMGateway.
- Реализовать MockLLMProvider для тестов/разработки.
- Реализовать адаптер YandexGPT провайдера, используя только настройки окружения.
- Добавить обработку timeout/retry/ошибок на границе gateway.
- Не раскрывать API-ключи в логах или ответах.

---

## Явно не делать

Не делать:

- вызывать LLM из бизнес-сервисов пока, если это не протестировано с mock
- хранить реальные секреты
- помещать токены в frontend
- реализовывать синтез ответов
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

- Вызывающие бизнес-код могут зависеть от интерфейса LLMGateway.
- Тесты используют MockLLMProvider.
- Yandex провайдер читает секреты только из env/settings.
- Реальный LLM-вызов не требуется в тестах.
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
- следующая задача: `TASK_016_query_understanding.md`;
- готовность к коммиту.
