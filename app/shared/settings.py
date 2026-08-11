from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKENDS_NOTIFICACAO_VALIDOS = {"log", "smtp"}
_CAMPOS_SMTP_OBRIGATORIOS = (
    "smtp_host",
    "smtp_port",
    "smtp_usuario",
    "smtp_senha",
    "smtp_remetente",
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str
    environment: str
    database_url: str

    jwt_secret_key: str
    jwt_expiracao_minutos: int

    seed_admin_email: str
    seed_admin_senha: str
    seed_atendente_email: str
    seed_atendente_senha: str
    seed_mecanico_email: str
    seed_mecanico_senha: str

    # notificacao_backend é obrigatório (segue o padrão do resto das configs), mas os
    # campos smtp_* são condicionalmente obrigatórios - só fazem sentido quando o
    # backend escolhido é "smtp". Por isso ficam com default None em vez de seguir a
    # regra geral "todo campo é obrigatório": aqui, "obrigatório" depende de outro campo,
    # o que só o model_validator abaixo consegue expressar.
    notificacao_backend: str
    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_usuario: str | None = None
    smtp_senha: str | None = None
    smtp_remetente: str | None = None

    @model_validator(mode="after")
    def _validar_configuracao_de_notificacao(self) -> "Settings":
        if self.notificacao_backend not in _BACKENDS_NOTIFICACAO_VALIDOS:
            opcoes = ", ".join(sorted(_BACKENDS_NOTIFICACAO_VALIDOS))
            raise ValueError(
                f"notificacao_backend deve ser um de: {opcoes} "
                f"(recebido: {self.notificacao_backend!r})"
            )

        if self.notificacao_backend == "smtp":
            faltando = [
                campo for campo in _CAMPOS_SMTP_OBRIGATORIOS if getattr(self, campo) is None
            ]
            if faltando:
                raise ValueError(
                    "notificacao_backend=smtp exige os campos: " + ", ".join(faltando)
                )

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
