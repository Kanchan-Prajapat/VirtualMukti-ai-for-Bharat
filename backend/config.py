from typing import List
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_db_name: str
    mongodb_encryption_key: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    firebase_credentials_path: str
    firebase_database_url: str

    gemini_api_key: str
    aes_encryption_key: str
    lstm_model_path: str

    retrain_schedule: str = "weekly"

    cors_origins: str = ""

    app_name: str = "VirtualMukti"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    app_env: str = "development"   # ✅ ADD THIS (used in uvicorn)

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=()  # ✅ removes pydantic warnings
    )

    @property
    def cors_origins_list(self) -> List[str]:
        if not self.cors_origins:
            return []
        return [o.strip() for o in self.cors_origins.split(",")]

settings = Settings()
