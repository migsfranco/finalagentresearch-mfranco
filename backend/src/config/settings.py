"""Application settings using Pydantic BaseSettings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    environment: str = "development"
    log_level: str = "INFO"

    # LLM Provider (optional at startup, required for chat)
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.0

    # Search Tools API Keys
    tavily_api_key: str | None = None
    serp_api_key: str | None = None

    # LangSmith Tracing (Optional)
    langchain_tracing_v2: bool = False
    langchain_api_key: str | None = None
    langchain_project: str = "agente-investigador"

    # Vector Store Configuration
    chroma_persist_directory: str = "./data/chroma"
    chroma_collection_name: str = "apa_documents"

    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retriever_k: int = 3

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
