from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "StockSense AI"
    debug: bool = False
    cors_origins: list[str] = ["http://localhost:3000"]

    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/stocksense"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    jwt_refresh_expire_days: int = 7

    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"

    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000

    finnhub_api_key: str = ""
    admin_email: str = "admin@stocksense.ai"

    class Config:
        env_file = ".env"


settings = Settings()
