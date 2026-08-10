from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# placeholders de desenvolvimento - nunca podem sobreviver fora de ENVIRONMENT=local,
# ver _rejeitar_segredos_padrao_fora_de_local abaixo. Ficam num nome próprio (em vez de
# só o literal inline) para o validador comparar sem duplicar o valor.
_JWT_SECRET_KEY_PLACEHOLDER = "change-me-in-production-please-set-env-var"  # noqa: S105
_SEED_ADMIN_SENHA_PLACEHOLDER = "admin123"  # noqa: S105 - placeholder, não é senha real


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Oficina Mecânica API"
    environment: str = "local"
    database_url: str = "postgresql+asyncpg://oficina:oficina@localhost:5432/oficina"

    # placeholder, sempre sobrescrito por env var em produção - com >=32 bytes para não
    # cair abaixo do mínimo recomendado (RFC 7518 §3.2) para HS256 caso alguém esqueça de
    # configurar a variável de ambiente. E, mesmo assim, fora de local o uso do valor
    # padrão é bloqueado no startup (ver validador abaixo) - defesa em profundidade.
    jwt_secret_key: str = _JWT_SECRET_KEY_PLACEHOLDER  # noqa: S105
    jwt_expiracao_minutos: int = 60

    seed_admin_email: str = "admin@oficina.com.br"
    seed_admin_senha: str = _SEED_ADMIN_SENHA_PLACEHOLDER

    @model_validator(mode="after")
    def _rejeitar_segredos_padrao_fora_de_local(self) -> "Settings":
        if self.environment == "local":
            return self

        if self.jwt_secret_key == _JWT_SECRET_KEY_PLACEHOLDER:
            raise ValueError(
                "JWT_SECRET_KEY precisa ser definida via variável de ambiente fora de "
                "ENVIRONMENT=local (o placeholder de desenvolvimento não pode ser usado)."
            )
        if self.seed_admin_senha == _SEED_ADMIN_SENHA_PLACEHOLDER:
            raise ValueError(
                "SEED_ADMIN_SENHA precisa ser definida via variável de ambiente fora de "
                "ENVIRONMENT=local (o placeholder de desenvolvimento não pode ser usado)."
            )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
