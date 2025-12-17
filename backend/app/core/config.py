from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration.

    Uses environment variables and optional .env file.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "MA EV ChargeMap API"
    env: str = "dev"

    # Postgres
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/evchargemap"

    # CORS
    cors_allow_origins: str = "http://localhost:3000"

    # Model artifact (stored as JSON, not pickle)
    model_path: str = "models/site_demand_model.json"


settings = Settings()
