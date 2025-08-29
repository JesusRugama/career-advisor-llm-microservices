import os
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration - will be overridden by environment variables
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/career_advisor"

    feign_client_url: str = "http://localhost:8000"
    feign_client_timeout: int = 10
    
    # XAI API Configuration
    xai_api_key: str = "test-key-not-used"  # Default for testing
    xai_base_url: str = "https://api.x.ai/v1"
    xai_model: str = "grok-4-latest"
    
    # Application Configuration
    debug: bool = False

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()

# Debug: Print the actual database URL being used
print(f"🔍 Database URL from settings: {settings.database_url}")
print(f"🔍 DATABASE_URL env var: {os.getenv('DATABASE_URL', 'NOT SET')}")
