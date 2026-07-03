"""Application settings loaded from environment variables.

Secrets must live only in `.env` and never be committed.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "rd-knowledge-map-backend"
    debug: bool = False

    # PostgreSQL — placeholder, not wired yet
    database_url: str = "postgresql+asyncpg://postgres:change_me@localhost:5432/rd_knowledge_map"

    # Redis — placeholder
    redis_url: str = "redis://localhost:6379/0"

    # Elasticsearch — placeholder
    elasticsearch_url: str = "http://localhost:9200"

    # Neo4j — placeholder
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "change_me"

    # MinIO — placeholder
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "change_me"
    minio_bucket: str = "rd-documents"
    minio_secure: bool = False

    # LLM — placeholder
    llm_provider: str = "mock"
    yandex_api_key: str = "change_me"
    yandex_folder_id: str = "change_me"
    yandex_llm_model: str = "yandexgpt-lite"


settings = Settings()
