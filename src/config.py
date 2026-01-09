"""Configuration management for the Databricks Metadata Chat Assistant."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Azure OpenAI Configuration
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment_name: str
    azure_openai_api_version: str = "2023-12-01-preview"
    
    # PostgreSQL Configuration
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "databricks_metadata"
    postgres_user: str = "readonly_user"
    postgres_password: str = "readonly_pass"
    
    # Application Settings
    max_query_results: int = 100
    log_level: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @property
    def database_url(self) -> str:
        """Construct database URL from components."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()
