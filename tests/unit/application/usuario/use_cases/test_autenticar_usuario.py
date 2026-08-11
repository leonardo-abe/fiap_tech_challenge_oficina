import pytest

from app.application.usuario.dtos import AutenticarUsuarioInput
from app.application.usuario.use_cases import AutenticarUsuarioUseCase
from app.domain.usuario.entities import Usuario
from app.domain.usuario.exceptions import CredenciaisInvalidasError
from app.domain.usuario.value_objects import Perfil
from tests.unit.application.fakes import (
    FakePasswordHasher,
    FakeTokenProvider,
    FakeUsuarioRepository,
)


async def _criar_usuario(repositorio, hasher, ativo=True):
    return await repositorio.criar(
        Usuario(
            nome="João",
            email="joao@x.com",
            senha_hash=hasher.hash("segredo123"),
            perfil=Perfil.MECANICO,
            ativo=ativo,
        )
    )


_HASH_SEM_CORRESPONDENCIA = "hash(nunca-bate)"


async def test_autenticar_usuario_sucesso():
    repositorio = FakeUsuarioRepository()
    hasher = FakePasswordHasher()
    token_provider = FakeTokenProvider()
    await _criar_usuario(repositorio, hasher)
    use_case = AutenticarUsuarioUseCase(
        repositorio, hasher, token_provider, _HASH_SEM_CORRESPONDENCIA
    )

    resultado = await use_case.executar(
        AutenticarUsuarioInput(email="joao@x.com", senha="segredo123")
    )

    assert resultado.access_token == "token-1-MECANICO"
    assert resultado.token_type == "bearer"


async def test_autenticar_usuario_inexistente_levanta_erro():
    use_case = AutenticarUsuarioUseCase(
        FakeUsuarioRepository(),
        FakePasswordHasher(),
        FakeTokenProvider(),
        _HASH_SEM_CORRESPONDENCIA,
    )

    with pytest.raises(CredenciaisInvalidasError):
        await use_case.executar(AutenticarUsuarioInput(email="ninguem@x.com", senha="qualquer"))


async def test_autenticar_usuario_com_senha_errada_levanta_erro():
    repositorio = FakeUsuarioRepository()
    hasher = FakePasswordHasher()
    await _criar_usuario(repositorio, hasher)
    use_case = AutenticarUsuarioUseCase(
        repositorio, hasher, FakeTokenProvider(), _HASH_SEM_CORRESPONDENCIA
    )

    with pytest.raises(CredenciaisInvalidasError):
        await use_case.executar(AutenticarUsuarioInput(email="joao@x.com", senha="errada"))


async def test_autenticar_usuario_inativo_levanta_erro():
    repositorio = FakeUsuarioRepository()
    hasher = FakePasswordHasher()
    await _criar_usuario(repositorio, hasher, ativo=False)
    use_case = AutenticarUsuarioUseCase(
        repositorio, hasher, FakeTokenProvider(), _HASH_SEM_CORRESPONDENCIA
    )

    with pytest.raises(CredenciaisInvalidasError):
        await use_case.executar(AutenticarUsuarioInput(email="joao@x.com", senha="segredo123"))
