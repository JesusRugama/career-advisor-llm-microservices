from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/career_advisor"
    
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
