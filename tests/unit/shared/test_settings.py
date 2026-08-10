import pytest

from app.shared.settings import Settings


def test_jwt_secret_key_e_obrigatoria_mesmo_em_local(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    with pytest.raises(ValueError, match="jwt_secret_key"):
        Settings(_env_file=None, environment="local", seed_admin_senha="qualquer-coisa")


def test_seed_admin_senha_e_obrigatoria_mesmo_em_local(monkeypatch):
    monkeypatch.delenv("SEED_ADMIN_SENHA", raising=False)

    with pytest.raises(ValueError, match="seed_admin_senha"):
        Settings(
            _env_file=None,
            environment="local",
            jwt_secret_key="uma-chave-bem-longa-e-aleatoria-1234567890",
        )


def test_settings_com_segredos_explicitos_funciona_em_qualquer_ambiente():
    config = Settings(
        _env_file=None,
        environment="production",
        jwt_secret_key="uma-chave-bem-longa-e-aleatoria-1234567890",
        seed_admin_senha="uma-senha-forte-qualquer",
    )

    assert config.environment == "production"
    assert config.jwt_secret_key == "uma-chave-bem-longa-e-aleatoria-1234567890"
