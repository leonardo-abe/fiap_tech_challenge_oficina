from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Oficina Mecânica API"
    environment: str = "local"
    database_url: str = "postgresql+asyncpg://oficina:oficina@localhost:5432/oficina"

    # placeholder, sempre sobrescrito por env var em produção - mas com >=32 bytes mesmo
    # assim, para não cair abaixo do mínimo recomendado (RFC 7518 §3.2) para HS256 caso
    # alguém esqueça de configurar a variável de ambiente.
    jwt_secret_key: str = "change-me-in-production-please-set-env-var"  # noqa: S105
    jwt_expiracao_minutos: int = 60

    seed_admin_email: str = "admin@oficina.com.br"
    seed_admin_senha: str = "admin123"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
