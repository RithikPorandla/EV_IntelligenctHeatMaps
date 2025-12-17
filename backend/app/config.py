"""
Configuration settings for the MA EV ChargeMap backend.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://evcharge:evcharge123@localhost:5432/evcharge"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://frontend:3000"]
    
    # Project metadata
    project_name: str = "MA EV ChargeMap API"
    project_description: str = (
        "API for EV charging siting intelligence in Massachusetts. "
        "A personal portfolio project demonstrating data analysis, "
        "data engineering, and ML skills."
    )
    version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
