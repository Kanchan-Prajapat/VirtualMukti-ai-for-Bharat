from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List


class Settings(BaseSettings):
    # App
    app_name: str = "VirtualMukti"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # Database
    mongodb_uri: str
    mongodb_db_name: str

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # AI
    gemini_api_key: str

    aes_encryption_key: str = "your-32-character-secret-key-1234"

    # CORS
    cors_origins: str = ""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        if not self.cors_origins:
            return []
        return [o.strip() for o in self.cors_origins.split(",")]


settings = Settings()