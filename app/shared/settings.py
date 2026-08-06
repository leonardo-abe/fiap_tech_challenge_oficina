from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Oficina Mecânica API"
    environment: str = "local"
    database_url: str = "postgresql+asyncpg://oficina:oficina@localhost:5432/oficina"

    jwt_secret_key: str = "change-me-in-production"  # noqa: S105 - placeholder, sobrescrito por env var
    jwt_expiracao_minutos: int = 60

    seed_admin_email: str = "admin@oficina.com.br"
    seed_admin_senha: str = "admin123"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
