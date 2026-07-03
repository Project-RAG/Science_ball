# System Design Document: R&D Knowledge Map
## 1. Назначение системы
R&D Knowledge Map — система поиска, анализа и построения карты знаний для горно-металлургических исследований.
Система принимает научные публикации, внутренние отчеты, патенты, экспериментальные протоколы, таблицы и справочники, извлекает из них сущности, числовые параметры, связи, факты и источники, после чего позволяет исследователям задавать сложные вопросы на русском или английском языке.
Ключевой результат системы: структурированный ответ с источниками, уровнем доверия, противоречиями, пробелами в знаниях и связями графа.
---
## 2. Главные архитектурные принципы
1. Elasticsearch — основной слой полнотекстового, векторного, числового и фильтруемого поиска.
2. Neo4j — отдельное графовое хранилище для обходов знаний и визуализации связей.
3. PostgreSQL — транзакционные данные, пользователи, роли, документы, версии фактов, аудит.
4. MinIO — оригинальные документы, распарсенные артефакты, экспорты.
5. Redis + Celery — очереди, фоновые задачи, кеширование.
6. LLM не является источником истины.
7. Все факты должны трассироваться до документа и конкретного чанка.
8. Числовые параметры извлекаются детерминированно через regex/
parser + нормализацию единиц.
9. YandexGPT используется через backend-
only LLMGateway, без прямой зависимости бизнес-логики от провайдера.
10. Все поисковые запросы обязаны учитывать `access_level`.
---
## 3. Функциональные требования
Система должна поддерживать:
1. Загрузку документов:
   - PDF;
   - DOCX;
   - XLSX/CSV;
   - Markdown/TXT;
   - патенты;
   - внутренние отчеты;
   - экспериментальные протоколы;
   - справочники материалов, оборудования и единиц измерения.
2. Извлечение сущностей:
   - `Material`;
   - `Process`;
   - `Equipment`;
   - `Property`;
   - `Experiment`;
   - `Publication`;
   - `Patent`;
   - `Report`;
   - `Expert`;
   - `Organization`;
   - `Facility`;
   - `Method`;
   - `Technology`;
   - `Location`;
   - `NumericCondition`;
   - `Conclusion`.
3. Извлечение связей:
   - `USES_MATERIAL`;
   - `APPLIES_TO`;
   - `OPERATES_AT_CONDITION`;
   - `PRODUCES_OUTPUT`;
   - `DESCRIBED_IN`;
   - `VALIDATED_BY`;
   - `CONTRADICTS`;
   - `AUTHORED_BY`;
   - `EXPERT_IN`;
   - `LOCATED_IN`;
   - `HAS_RESULT`;
   - `HAS_LIMITATION`.
4. Извлечение числовых условий:
   - концентрация;
   - температура;
   - давление;
   - скорость потока;
   - pH;
   - производительность;
   - CAPEX;
   - OPEX;
   - сухой остаток;
   - извлечение металла;
   - год публикации.
5. Гибридный поиск:
   - BM25 через Elasticsearch;
   - vector search через `dense_vector`;
   -
 фильтры по материалам, процессам, географии, году, типу источника, уровню доверия;
   - фильтры по числовым диапазонам;
   - сравнение отечественной и зарубежной практики.
6. Графовую навигацию:
   - материал → процесс → оборудование → результат;
   - публикация → эксперимент → вывод;
   - эксперт → область → источники;
   - технология → ограничения → география.
7. Генерацию ответов:
   - краткий вывод;
   - таблица методов;
   - evidence;
   - источники;
   - confidence;
   - contradictions;
   - knowledge gaps;
   - related experts;
   - graph fragment.
8. Ручную верификацию:
   - добавление сущностей;
   - редактирование связей;
   - подтверждение/отклонение фактов;
   - история версий;
   - аудит изменений.
9. Ролевой доступ:
   - `admin`;
   - `researcher`;
   - `analyst`;
   - `manager`;
   - `external_partner`.
---
## 4. Нефункциональные требования
1. Ответ на сложный запрос: до 3–5 секунд при объеме до 1 млн сущностей.
2. Поддержка русского и английского языков.
3. Возможность MVP-развертывания на одной машине через Docker Compose.
4. Использование open-source компонентов там, где это возможно.
5. Поддержка YandexGPT API как основного LLM-провайдера для хакатона.
6. Возможность fallback на локальную LLM.
7. Трассируемость каждого факта до источника.
8. Версионирование фактов.
9. Расширяемость на новые домены:
   - гидрометаллургия;
   - пирометаллургия;
   - экология;
   - переработка отходов;
   - редкоземельные элементы.
---
## 5. Технологический стек
### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Celery
- Redis
### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- React Flow
### Хранилища
- PostgreSQL — транзакционные данные, RBAC, аудит, версии.
- Elasticsearch — полнотекстовый, векторный, числовой и аналитический поиск.
- Neo4j Community Edition — граф знаний.
- MinIO — документы и экспорты.
- Redis — очереди, кеш, статусы задач.
### NLP и LLM
Embeddings для MVP:
- основной вариант: `intfloat/multilingual-e5-small`;
- альтернатива: `sentence-transformers/paraphrase-multilingual-MiniLM-
L12-v2`.
LLM:
-
 основной провайдер для хакатона: Yandex Cloud Foundation Models / YandexGPT;
- рекомендуемая модель MVP: `yandexgpt-lite`;
- для сложных обзоров: `yandexgpt`;
- fallback: Qwen2.5-3B/7B через Ollama, llama.cpp или vLLM.
NER и извлечение фактов:
- словари домена;
- регулярные выражения;
- spaCy;
- опционально DeepPavlov/ruBERT;
- LLM только как вспомогательный интерпретатор.
---
## 6. Высокоуровневая архитектура
```text
Frontend React
    |
    v
FastAPI Backend
    |
    +--> PostgreSQL: users, roles, documents, facts, versions, audit
    |
    +--> Elasticsearch: docs, chunks, entities, facts, vectors, filters
    |
    +--> Neo4j: knowledge graph, graph traversal, contradictions
    |
    +--> Redis: queues, cache, job status
    |
    +--> MinIO: source files, parsed artifacts, exports
    |
    +--> LLMGateway
            |
            +--> YandexGPT API
            |
            +--> Local LLM fallback
            |
            +--> Mock provider for tests
---
    7. Основные backend-сервисы
      API Service
Отвечает за:
  * HTTP API;
  * авторизацию;
  * загрузку документов;
  * запуск фоновых задач;
  * поиск;
  * генерацию ответов;
  * работу с графом;
  * экспорт отчетов;
  * аудит действий.
Основные routes:
auth.py
documents.py
ingestion.py
search.py
answers.py
graph.py
facts.py
experts.py
exports.py
admin.py
health.py
---
      Ingestion Service
Pipeline:
upload file
→ save original to MinIO
→ create document metadata in PostgreSQL
→ detect file type
→ parse text/tables/images
→ OCR if needed
→ split into chunks
→ detect language
→ store chunks
→ send chunks to NLP pipeline
---
Парсеры:
  * PDF: pymupdf, pdfplumber;
  * DOCX: python-docx;
  * XLSX: openpyxl, pandas;
  * CSV: pandas;
  * HTML/XML: beautifulsoup4;
  * OCR: tesseract.
---
      NLP Pipeline
Pipeline:
chunk text
→ clean text
→ detect language
→ extract entities
→ extract numeric conditions
→ normalize terms
→ normalize units
→ extract relations
→ calculate confidence
→ create facts
→ index to Elasticsearch
→ write graph to Neo4j
---
Правила:
  * числа извлекать детерминированно;
  * единицы измерения нормализовать;
  * LLM не должна быть единственным источником чисел;
  * каждый факт должен ссылаться на document_id и chunk_id.
---
      Search Service
Pipeline:
user query
→ language detection
→ query understanding
→ extract filters
→ extract numeric constraints
→ build Elasticsearch BM25 query
→ build Elasticsearch vector query
→ merge results
→ apply access filters
→ rerank
→ fetch graph neighborhood from Neo4j
→ return ranked evidence
---
      Answer Synthesis Service
Вход:
  * исходный вопрос;
  * найденные chunks;
  * найденные facts;
  * graph neighborhood;
  * contradictions;
  * knowledge gaps;
  * user permissions.
Выход:
{
  "short_answer": "Краткий вывод",
  "methods": [],
  "evidence": [],
  "contradictions": [],
  "knowledge_gaps": [],
  "experts": [],
  "confidence": 0.82,
  "sources": []
}
---
Правило: LLM отвечает только на основании переданного evidence.
---
    8. Интеграция Yandex Studio / YandexGPT
      Назначение
YandexGPT используется для:
 1. Query understanding.
 2. Классификации intent.
 3. Переформулирования запроса.
 4. Синтеза финального ответа по evidence.
 5. Опционального relation extraction.
 6. Опциональных аннотаций документов.
YandexGPT не используется как источник истины.
      Абстракция
Все обращения к LLM идут через единый интерфейс:
LLMProvider
  ├── YandexLLMProvider
  ├── LocalLLMProvider
  └── MockLLMProvider
---
Бизнес-логика не должна напрямую вызывать Yandex API.
      Конфигурация окружения
LLM_PROVIDER=yandex
YANDEX_API_KEY=change_me
YANDEX_FOLDER_ID=change_me
YANDEX_LLM_MODEL=yandexgpt-lite
YANDEX_LLM_MODEL_VERSION=latest
YANDEX_LLM_ENDPOINT=https://llm.api.cloud.yandex.net/foundationModels/v1/completion
YANDEX_EMBEDDINGS_ENABLED=false
YANDEX_EMBEDDING_QUERY_MODEL=text-search-query
YANDEX_EMBEDDING_DOC_MODEL=text-search-doc
YANDEX_EMBEDDING_ENDPOINT=https://llm.api.cloud.yandex.net/foundationModels/v1/textEmbedding
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=3000
LLM_TIMEOUT_SECONDS=60
LLM_MAX_RETRIES=2
LOCAL_LLM_ENDPOINT=http://ollama:11434
LOCAL_LLM_MODEL=qwen2.5:7b-instruct
---
Запрещено хранить API key:
  * во frontend;
  * в публичном config;
  * в git;
  * в Docker image layer;
  * в README;
  * в скриншотах презентации.
      Model URI
Формат:
gpt://<folder_id>/yandexgpt-lite/latest
gpt://<folder_id>/yandexgpt/latest
---
Для MVP использовать yandexgpt-lite.
      Backend modules
backend/app/services/llm/
  base.py
  yandex_provider.py
  local_provider.py
  mock_provider.py
  llm_gateway.py
  prompts.py
  errors.py
backend/app/services/embeddings/
  base.py
  local_embedding_provider.py
  yandex_embedding_provider.py
  embedding_gateway.py
---
      LLMProvider interface
from abc import ABC, abstractmethod
class LLMProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 3000,
        json_mode: bool = False,
    ) -> str:
        pass
class LLMProviderError(Exception):
    pass
---
      Yandex provider behavior
Yandex provider должен:
  * формировать modelUri;
  * отправлять Authorization: Api-Key <secret>;
  * передавать messages в формате Yandex Foundation Models;
  * обрабатывать 401/403, 429, 5xx, timeout;
  * не логировать токены и Authorization headers;
  * возвращать только текст ответа;
  * выбрасывать LLMProviderError при ошибках.
      Query Understanding через YandexGPT
Prompt должен требовать валидный JSON без markdown.
Ожидаемая структура:
{
  "intent": "technology_review",
  "materials": ["nickel", "catholyte"],
  "processes": ["electrowinning"],
  "equipment": [],
  "properties": ["flow_velocity"],
  "geography": [],
  "practice_region": "foreign",
  "year_from": null,
  "year_to": null,
  "numeric_conditions": [],
  "source_types": ["publication", "patent", "report"],
  "requested_output": {
    "include_graph": true,
    "include_experts": true,
    "include_contradictions": true
  }
}
---
После LLM:
 1. Валидировать JSON через Pydantic.
 2. При ошибке использовать deterministic fallback.
 3. Числовые условия дополнительно проверять NumericExtractor.
      Answer Synthesis через YandexGPT
Prompt rules:
Отвечай только на основании переданных источников.
Если данных недостаточно, явно напиши, что данных недостаточно.
Не придумывай числовые значения.
Для каждого технического утверждения указывай source_id.
Не используй документы, к которым у пользователя нет доступа.
---
      Ошибки Yandex API
Поведение:
query understanding failed
→ fallback на regex/dictionary parser
answer synthesis failed
→ вернуть найденные evidence и сообщение, что генерация ответа недоступна
relation extraction failed
→ сохранить partial_success ingestion job
---
    9. Доменная онтология
      Типы узлов
Material
Process
Equipment
Property
Condition
Experiment
Publication
Patent
Report
Expert
Organization
Facility
Technology
Method
Result
Conclusion
Location
Unit
EconomicIndicator
EnvironmentalIndicator
---
      Пример Material
{
  "id": "mat_nickel",
  "name": "никель",
  "canonical_name": "nickel",
  "aliases": ["Ni", "никелевая руда", "nickel ore"],
  "material_type": "metal"
}
---
      Пример Process
{
  "id": "proc_electrowinning",
  "name": "электроэкстракция",
  "canonical_name": "electrowinning",
  "aliases": ["electrowinning", "электролитическое извлечение"],
  "domain": "hydrometallurgy"
}
---
      Пример NumericCondition
{
  "id": "cond_123",
  "property": "temperature",
  "value": 65,
  "min_value": null,
  "max_value": null,
  "unit": "C",
  "raw_text": "температура 65 °C",
  "normalized_value_si": 338.15
}
---
      Пример Fact
{
  "id": "fact_123",
  "subject_id": "proc_electrowinning",
  "predicate": "OPERATES_AT_CONDITION",
  "object_id": "cond_123",
  "source_document_id": "doc_456",
  "source_chunk_id": "chunk_789",
  "confidence": 0.84,
  "verification_status": "machine_extracted",
  "created_at": "2025-07-01T10:00:00Z",
  "updated_at": "2025-07-01T10:00:00Z"
}
---
    10. Модель доверия
Каждый факт имеет:
{
  "confidence": 0.0,
  "verification_status": "machine_extracted | expert_verified | rejected | outdated | contradicted",
  "source_type": "publication | internal_report | patent | experiment | handbook",
  "source_reliability": 0.0,
  "extraction_method": "regex | dictionary | ner_model | llm | manual",
  "verified_by": "user_id",
  "verified_at": "timestamp",
  "valid_from": "date",
  "valid_to": "date",
  "version": 1
}
---
Формула MVP:
fact_confidence = 0.35 * extraction_confidence + 0.25 * source_reliability + 0.20 * supporting_sources_score + 0.20 * expert_verification_score
---
Ограничение: факт, извлеченный только LLM, не должен получать confidence выше 0.65 без экспертной проверки.
---
    11. Elasticsearch design
      Индексы
rd_docs_v1
rd_chunks_v1
rd_entities_v1
rd_facts_v1
rd_experiments_v1
rd_experts_v1
---
      rd_docs_v1
Назначение:
  * метаданные документов;
  * фильтры по типу, году, географии, доступу.
Ключевые поля:
{
  "document_id": "doc_001",
  "title": "Nickel electrowinning review",
  "source_type": "publication",
  "language": "en",
  "year": 2022,
  "authors": ["Ivan Petrov"],
  "organizations": ["Institute A"],
  "geography": ["Canada"],
  "practice_region": "foreign",
  "domains": ["hydrometallurgy"],
  "access_level": "internal"
}
---
      rd_chunks_v1
Назначение:
  * полнотекстовый поиск;
  * vector search;
  * RAG context.
Ключевые поля:
{
  "chunk_id": "chunk_001",
  "document_id": "doc_001",
  "text": "Catholyte circulation rate of 0.15-0.25 m/s...",
  "language": "en",
  "page": 12,
  "section": "Results",
  "year": 2022,
  "source_type": "publication",
  "geography": ["Canada"],
  "practice_region": "foreign",
  "access_level": "internal",
  "entities": ["nickel", "electrowinning", "catholyte"],
  "numeric_conditions": [
    {
      "property": "flow_velocity",
      "min_value": 0.15,
      "max_value": 0.25,
      "unit": "m/s"
    }
  ],
  "embedding": [0.01, 0.02, 0.03]
}
---
      rd_facts_v1
Назначение:
  * поиск фактов;
  * фильтры по числовым условиям;
  * evidence layer.
Ключевые поля:
{
  "fact_id": "fact_001",
  "subject": {
    "id": "proc_electrowinning",
    "type": "Process",
    "name": "electrowinning"
  },
  "predicate": "OPERATES_AT_CONDITION",
  "object": {
    "id": "cond_flow_001",
    "type": "Condition",
    "name": "catholyte flow velocity"
  },
  "numeric": {
    "property": "flow_velocity",
    "min_value": 0.15,
    "max_value": 0.25,
    "unit": "m/s"
  },
  "source_document_id": "doc_001",
  "source_chunk_id": "chunk_001",
  "confidence": 0.87,
  "verification_status": "machine_extracted",
  "access_level": "internal"
}
---
      Mapping rules
Использовать:
keyword       для id, enum, canonical_name
text          для русского и английского поиска
dense_vector  для embeddings
float         для числовых значений
integer       для года
date          для дат
nested        для numeric_conditions
---
Анализаторы:
  * russian;
  * english;
  * icu_folding;
  * synonym filter.
Не смешивать embeddings разных размерностей в одном индексе. При смене embedding provider создавать новый индекс, например rd_chunks_v2.
---
    12. PostgreSQL design
Основные таблицы:
users
roles
user_roles
documents
document_versions
ingestion_jobs
chunks
entities
facts
fact_versions
fact_reviews
audit_log
saved_queries
notifications
exports
---
      documents
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    source_type TEXT NOT NULL,
    language TEXT,
    year INT,
    access_level TEXT NOT NULL,
    minio_bucket TEXT NOT NULL,
    minio_object_key TEXT NOT NULL,
    checksum TEXT NOT NULL,
    created_by UUID,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
---
      facts
CREATE TABLE facts (
    id UUID PRIMARY KEY,
    subject_id TEXT NOT NULL,
    subject_type TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object_id TEXT NOT NULL,
    object_type TEXT NOT NULL,
    source_document_id UUID NOT NULL,
    source_chunk_id UUID,
    confidence NUMERIC(4,3) NOT NULL,
    verification_status TEXT NOT NULL,
    created_by UUID,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
---
      fact_versions
CREATE TABLE fact_versions (
    id UUID PRIMARY KEY,
    fact_id UUID NOT NULL,
    version INT NOT NULL,
    payload JSONB NOT NULL,
    changed_by UUID,
    change_reason TEXT,
    created_at TIMESTAMP NOT NULL
);
---
      audit_log
CREATE TABLE audit_log (
    id UUID PRIMARY KEY,
    user_id UUID,
    action TEXT NOT NULL,
    entity_type TEXT,
    entity_id TEXT,
    payload JSONB,
    created_at TIMESTAMP NOT NULL
);
---
    13. Neo4j design
      Constraints
CREATE CONSTRAINT material_id IF NOT EXISTS
FOR (n:Material) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT process_id IF NOT EXISTS
FOR (n:Process) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT publication_id IF NOT EXISTS
FOR (n:Publication) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT experiment_id IF NOT EXISTS
FOR (n:Experiment) REQUIRE n.id IS UNIQUE;
---
      Основные связи
(Material)-[:USED_IN]->(Process)
(Process)-[:USES_MATERIAL]->(Material)
(Process)-[:USES_EQUIPMENT]->(Equipment)
(Process)-[:OPERATES_AT_CONDITION]->(Condition)
(Process)-[:PRODUCES]->(Material)
(Experiment)-[:VALIDATES]->(Conclusion)
(Experiment)-[:DESCRIBED_IN]->(Publication)
(Publication)-[:AUTHORED_BY]->(Expert)
(Expert)-[:EXPERT_IN]->(Process)
(Technology)-[:APPLIES_TO]->(Material)
(Technology)-[:HAS_LIMITATION]->(Condition)
(Conclusion)-[:CONTRADICTS]->(Conclusion)
(Facility)-[:LOCATED_IN]->(Location)
---
      Пример записи факта
MERGE (p:Process {id: $process_id})
SET p.name = $process_name,
    p.canonical_name = $process_canonical_name
MERGE (m:Material {id: $material_id})
SET m.name = $material_name,
    m.canonical_name = $material_canonical_name
MERGE (p)-[r:USES_MATERIAL]->(m)
SET r.fact_id = $fact_id,
    r.confidence = $confidence,
    r.source_document_id = $source_document_id,
    r.verification_status = $verification_status,
    r.updated_at = datetime()
---
    14. API endpoints
      Auth
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/auth/me
---
      Documents
POST   /api/v1/documents/upload
GET    /api/v1/documents
GET    /api/v1/documents/{document_id}
DELETE /api/v1/documents/{document_id}
GET    /api/v1/documents/{document_id}/chunks
GET    /api/v1/documents/{document_id}/facts
---
      Ingestion
POST /api/v1/ingestion/jobs
GET  /api/v1/ingestion/jobs/{job_id}
POST /api/v1/ingestion/jobs/{job_id}/retry
---
      Search
POST /api/v1/search
POST /api/v1/search/facts
POST /api/v1/search/experiments
POST /api/v1/search/experts
---
      Answers
POST /api/v1/answers
POST /api/v1/answers/literature-review
POST /api/v1/answers/compare-technologies
---
      Graph
GET  /api/v1/graph/node/{node_id}
POST /api/v1/graph/neighborhood
POST /api/v1/graph/path
POST /api/v1/graph/manual-node
POST /api/v1/graph/manual-edge
---
      Verification
GET  /api/v1/facts/pending-review
POST /api/v1/facts/{fact_id}/verify
POST /api/v1/facts/{fact_id}/reject
POST /api/v1/facts/{fact_id}/comment
---
      Export
POST /api/v1/exports/markdown
POST /api/v1/exports/pdf
POST /api/v1/exports/jsonld
GET  /api/v1/exports/{export_id}
---
    15. POST /api/v1/answers
      Request
{
  "query": "Какие технические решения организации циркуляции католита при электроэкстракции никеля описаны в мировой практике?",
  "filters": {
    "practice_region": "foreign",
    "year_from": 2015,
    "year_to": 2025,
    "min_confidence": 0.6
  },
  "options": {
    "include_graph": true,
    "include_experts": true,
    "include_contradictions": true
  }
}
---
      Response
{
  "answer": {
    "summary": "В мировой практике описаны несколько схем циркуляции католита...",
    "confidence": 0.81
  },
  "tables": [
    {
      "title": "Сравнение технических решений",
      "columns": ["Метод", "Скорость потока", "Оборудование", "География", "Источники"],
      "rows": []
    }
  ],
  "evidence": [
    {
      "source_document_id": "doc_001",
      "chunk_id": "chunk_001",
      "quote": "Catholyte circulation rate of 0.15-0.25 m/s...",
      "confidence": 0.87
    }
  ],
  "graph": {
    "nodes": [],
    "edges": []
  },
  "contradictions": [],
  "knowledge_gaps": [],
  "experts": []
}
---
    16. Frontend screens
      Search Page
Компоненты:
SearchInput
FilterPanel
SavedQueries
RecentDocuments
---
      Answer Page
AnswerSummary
EvidenceTable
TechnologyComparisonTable
SourceList
ConfidenceBadge
ContradictionPanel
KnowledgeGapPanel
RelatedExpertsPanel
GraphPreview
ExportButton
---
      Graph Page
GraphCanvas
NodeDetailsPanel
EdgeDetailsPanel
GraphFilters
PathFinder
ContradictionHighlightToggle
---
      Documents Page
UploadDropzone
DocumentMetadataForm
IngestionJobStatus
ParsingErrorsTable
DocumentTable
---
      Fact Review Page
PendingFactsQueue
FactDetails
SourceQuoteViewer
ApproveRejectButtons
EditFactForm
VersionHistory
---
      Dashboard Page
KnowledgeCoverageByDomain
ContradictionCount
LowConfidenceTopics
ActiveExperts
RecentlyAddedSources
DomesticVsForeignCoverage
---
    17. Рекомендуемая структура проекта
rd-knowledge-map/
  README.md
  docker-compose.yml
  .env.example
  Makefile
  docs/
    SDD.md
    API.md
    ONTOLOGY.md
    DEPLOYMENT.md
    DEMO_SCRIPT.md
    PROMPTS.md
  backend/
    app/
      main.py
      settings.py
      dependencies.py
      api/
        router.py
        routes/
          auth.py
          documents.py
          ingestion.py
          search.py
          answers.py
          graph.py
          facts.py
          experts.py
          exports.py
          admin.py
          health.py
      core/
        security.py
        permissions.py
        logging.py
        errors.py
        pagination.py
      db/
        postgres.py
        elasticsearch.py
        neo4j.py
        redis.py
        minio.py
      models/
      schemas/
      repositories/
      services/
        auth/
        ingestion/
        nlp/
        search/
        graph/
        answers/
        exports/
        notifications/
        llm/
        embeddings/
      workers/
        celery_app.py
        ingestion_tasks.py
        nlp_tasks.py
        indexing_tasks.py
        export_tasks.py
      ontology/
        materials.yml
        processes.yml
        equipment.yml
        properties.yml
        units.yml
        synonyms.yml
        relations.yml
      prompts/
        answer_synthesis.ru.md
        answer_synthesis.en.md
        relation_extraction.ru.md
        relation_extraction.en.md
        query_understanding.ru.md
        query_understanding.en.md
      elastic/
        mappings/
        analyzers/
      tests/
        unit/
        integration/
  frontend/
    src/
      api/
      components/
      pages/
      stores/
      types/
      styles/
  infra/
    docker/
    scripts/
  data/
    samples/
    processed/
  notebooks/
---
    18. Docker Compose services
Минимальный состав:
backend
frontend
worker
postgres
elasticsearch
neo4j
redis
minio
---
Опционально:
ollama
prometheus
grafana
kibana
---
Если используется YandexGPT, локальный LLM-контейнер не обязателен.
Backend и worker должны получать:
## environment:
  # LLM_PROVIDER: ${LLM_PROVIDER}
  # YANDEX_API_KEY: ${YANDEX_API_KEY}
  # YANDEX_FOLDER_ID: ${YANDEX_FOLDER_ID}
  # YANDEX_LLM_MODEL: ${YANDEX_LLM_MODEL}
  # YANDEX_LLM_MODEL_VERSION: ${YANDEX_LLM_MODEL_VERSION}
  # YANDEX_LLM_ENDPOINT: ${YANDEX_LLM_ENDPOINT}
---
    19. Безопасность
      RBAC roles
admin
researcher
analyst
manager
external_partner
---
      Permissions
documents:read
documents:write
documents:delete
facts:read
facts:verify
graph:edit
answers:create
exports:create
admin:manage_users
---
      Access levels
public
internal
confidential
restricted
---
Каждый документ, чанк и факт должен иметь access_level.
Elasticsearch-запросы всегда должны содержать access filter:
{
  "terms": {
    "access_level": ["public", "internal"]
  }
}
---
      YandexGPT security
 1. YANDEX_API_KEY хранить только в backend/worker environment.
 2. Frontend не должен знать токен.
 3. Все LLM-вызовы идут только через backend.
 4. В логах запрещены:
      * API key;
      * Authorization headers;
      * полный prompt с restricted/confidential данными.
 5. Для restricted документов отправлять в LLM только extracted facts, а не полный текст.
 6. В audit log можно писать:
      * user_id;
      * endpoint;
      * model;
      * duration;
      * token usage, если доступно;
      * document ids.
---
    20. Monitoring and logging
Использовать structured JSON logs.
Обязательные поля:
request_id
user_id
job_id
document_id
endpoint
duration_ms
status
---
Метрики:
api_request_duration_seconds
search_duration_seconds
graph_query_duration_seconds
ingestion_job_duration_seconds
documents_total
chunks_total
facts_total
failed_ingestion_jobs_total
llm_generation_duration_seconds
---
Для MVP достаточно FastAPI logs + Celery logs. Prometheus/Grafana можно добавить позже.
---
    21. Тестирование
      Unit tests
Обязательно покрыть:
numeric_extractor
unit_normalizer
term_normalizer
query_understanding
elastic_query_builder
confidence_service
llm_gateway
yandex_provider error handling
---
      Integration tests
Проверить:
upload document → parse → chunks
chunks → entities → facts
facts → Elasticsearch
facts → Neo4j
query → answer with sources
RBAC access filtering
LLM fallback behavior
---
      Evaluation dataset
Минимальный набор:
10 документов по обессоливанию воды
10 документов по электроэкстракции никеля
10 документов по распределению Au/Ag/МПГ
10 документов по закачке шахтных вод
---
Метрики:
entity precision
entity recall
numeric extraction accuracy
relation extraction precision
answer citation accuracy
search hit rate@10
---
    22. MVP scope
MVP должен включать:
 1. Загрузку PDF/DOCX/TXT.
 2. Парсинг текста.
 3. Разбиение на чанки.
 4. Словарное извлечение материалов, процессов, оборудования.
 5. Regex-извлечение числовых параметров.
 6. Нормализацию единиц.
 7. Индексацию в Elasticsearch.
 8. Запись базового графа в Neo4j.
 9. Natural language search.
10. Фильтры по году, географии, типу источника, confidence, числовым диапазонам.
11. Query understanding через YandexGPT с Pydantic-валидацией.
12. Fallback на deterministic parser при ошибке YandexGPT.
13. Генерацию ответа через YandexGPT только по evidence.
14. Простую визуализацию графа.
15. Ручную верификацию фактов.
16. Экспорт ответа в Markdown.
17. Безопасное хранение Yandex API key в .env.
---
    23. Что отложить после MVP
Не делать в первой версии:
 1. Полноценный OCR сложных сканов.
 2. Продвинутый reranker.
 3. OWL/SHACL-валидацию.
 4. Красивый PDF-экспорт.
 5. Сложные уведомления.
 6. Интеграцию с внешними патентными базами.
 7. Полное автоматическое выявление противоречий.
 8. BI-дашборды.
 9. Многоступенчатую модерацию.
10. SSO/LDAP.
---
    24. End-to-end сценарий
Пользователь спрашивает:
"Какие технические решения организации циркуляции католита при электроэкстракции никеля описаны в мировой практике, и какая скорость потока считается оптимальной?"
Система:
 1. Проверяет JWT и права доступа.
 2. Определяет язык.
 3. Через YandexGPT извлекает intent и структуру запроса.
 4. Валидирует JSON через Pydantic.
 5. Regex/parser дополнительно извлекает числовые условия.
 6. Ищет chunks и facts в Elasticsearch.
 7. Применяет access_level filters.
 8. Получает graph neighborhood из Neo4j.
 9. EvidenceBuilder собирает sources, facts, chunks, graph links.
10. ContradictionDetector ищет конфликтующие диапазоны.
11. AnswerService формирует строгий prompt.
12. LLMGateway вызывает YandexGPT.
13. Ответ валидируется и возвращается пользователю.
14. Действие пишется в audit_log.
---
    25. Приоритеты реализации
      Этап 1: Скелет
FastAPI
PostgreSQL
Elasticsearch
Neo4j
MinIO
Redis
Celery
Docker Compose
---
      Этап 2: Импорт документов
upload
parse
chunk
store metadata
show ingestion status
---
      Этап 3: NLP MVP
dictionary entity extraction
numeric regex extraction
unit normalization
term normalization
confidence scoring
---
      Этап 4: Индексация и граф
Elasticsearch indices
Neo4j nodes and edges
basic graph queries
---
      Этап 5: LLM integration
LLMGateway
YandexLLMProvider
MockLLMProvider
query understanding
answer synthesis
fallback behavior
---
      Этап 6: Поиск и ответы
hybrid search
evidence builder
citations
contradictions
knowledge gaps
---
      Этап 7: UI
search page
answer page
document upload
graph visualization
fact verification
---
      Этап 8: Demo polish
sample data
demo script
markdown export
dashboard mock
presentation
---
    26. Инструкции для менее мощной модели
При генерации кода строго соблюдать:
 1. Не смешивать бизнес-логику с API routes.
 2. Все обращения к PostgreSQL, Elasticsearch, Neo4j, Redis и MinIO выносить в clients/repositories.
 3. Все обращения к LLM выполнять только через LLMGateway.
 4. Не вызывать Yandex API напрямую из query_understanding.py, answer_service.py или routes.
 5. Каждый факт должен иметь source_document_id и желательно source_chunk_id.
 6. Все поисковые запросы должны учитывать access_level.
 7. Числовые значения всегда нормализовать.
 8. Не использовать LLM для точного извлечения чисел без regex/parser-проверки.
 9. Не генерировать ответ без evidence.
10. Не удалять старые версии фактов, а писать изменения в fact_versions.
11. В MVP сначала реализовать словари и regex, затем добавлять сложные модели.
12. Elasticsearch обязателен и является основным поисковым слоем.
13. Neo4j использовать для графовых обходов, а не заменять его Elasticsearch.
14. PostgreSQL использовать для транзакционной истины и аудита.
15. Не хранить секреты во frontend, git или Docker image.
16. Для тестов использовать MockLLMProvider.
17. При ошибке YandexGPT использовать fallback, а не ломать весь пользовательский сценарий.
18. LLM не должна придумывать факты, источники, числа или выводы.
