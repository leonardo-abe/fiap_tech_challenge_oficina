import pytest

from app.shared.settings import Settings

_CAMPOS_VALIDOS = {
    "app_name": "Oficina Mecânica API",
    "environment": "local",
    "database_url": "postgresql+asyncpg://oficina:oficina@localhost:5432/oficina",
    "jwt_secret_key": "uma-chave-bem-longa-e-aleatoria-1234567890",
    "jwt_expiracao_minutos": 60,
    "seed_admin_email": "admin@oficina.com.br",
    "seed_admin_senha": "uma-senha-forte-qualquer",
    "seed_atendente_email": "atendente@oficina.com.br",
    "seed_atendente_senha": "uma-senha-forte-qualquer",
    "seed_mecanico_email": "mecanico@oficina.com.br",
    "seed_mecanico_senha": "uma-senha-forte-qualquer",
    "notificacao_backend": "log",
}

_CAMPOS_SMTP = {
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_usuario": "oficina@gmail.com",
    "smtp_senha": "app-password",
    "smtp_remetente": "oficina@gmail.com",
}


@pytest.mark.parametrize("campo", sorted(_CAMPOS_VALIDOS))
def test_campo_e_obrigatorio(campo, monkeypatch):
    # nenhum campo tem default - tudo precisa vir de env var/.env, sempre, inclusive
    # valores que não são segredo (nome do app, URL do banco etc.), por decisão do time.
    monkeypatch.delenv(campo.upper(), raising=False)
    campos = {chave: valor for chave, valor in _CAMPOS_VALIDOS.items() if chave != campo}

    with pytest.raises(ValueError, match=campo):
        Settings(_env_file=None, **campos)


def test_settings_com_todos_os_campos_informados_funciona():
    config = Settings(_env_file=None, **_CAMPOS_VALIDOS)

    assert config.environment == "local"
    assert config.jwt_secret_key == "uma-chave-bem-longa-e-aleatoria-1234567890"


def test_settings_com_backend_invalido_levanta_erro():
    with pytest.raises(ValueError, match="notificacao_backend"):
        Settings(_env_file=None, **{**_CAMPOS_VALIDOS, "notificacao_backend": "carta-registrada"})


def test_settings_com_backend_smtp_sem_campos_smtp_levanta_erro():
    with pytest.raises(ValueError, match="smtp_host"):
        Settings(_env_file=None, **{**_CAMPOS_VALIDOS, "notificacao_backend": "smtp"})


def test_settings_com_backend_smtp_e_todos_os_campos_smtp_funciona():
    config = Settings(
        _env_file=None,
        **{**_CAMPOS_VALIDOS, "notificacao_backend": "smtp", **_CAMPOS_SMTP},
    )

    assert config.notificacao_backend == "smtp"
    assert config.smtp_host == "smtp.gmail.com"


def test_settings_com_backend_log_nao_exige_campos_smtp():
    config = Settings(_env_file=None, **_CAMPOS_VALIDOS)

    assert config.notificacao_backend == "log"
    assert config.smtp_host is None
