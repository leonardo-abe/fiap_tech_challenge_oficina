import pytest

from app.shared.settings import Settings


def test_settings_local_permite_placeholders():
    config = Settings(environment="local")

    assert config.jwt_secret_key == "change-me-in-production-please-set-env-var"
    assert config.seed_admin_senha == "admin123"


def test_settings_fora_de_local_com_jwt_secret_key_placeholder_levanta_erro():
    with pytest.raises(ValueError, match="JWT_SECRET_KEY"):
        Settings(environment="production", seed_admin_senha="uma-senha-forte-qualquer")


def test_settings_fora_de_local_com_seed_admin_senha_placeholder_levanta_erro():
    with pytest.raises(ValueError, match="SEED_ADMIN_SENHA"):
        Settings(
            environment="production",
            jwt_secret_key="uma-chave-bem-longa-e-aleatoria-1234567890",
        )


def test_settings_fora_de_local_com_segredos_customizados_nao_levanta_erro():
    config = Settings(
        environment="production",
        jwt_secret_key="uma-chave-bem-longa-e-aleatoria-1234567890",
        seed_admin_senha="uma-senha-forte-qualquer",
    )

    assert config.environment == "production"
