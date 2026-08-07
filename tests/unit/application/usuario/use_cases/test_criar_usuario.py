import pytest

from app.application.usuario.dtos import CriarUsuarioInput
from app.application.usuario.use_cases import CriarUsuarioUseCase
from app.domain.usuario.exceptions import EmailJaCadastradoError
from app.domain.usuario.value_objects import Perfil
from tests.unit.application.fakes import FakePasswordHasher, FakeUsuarioRepository


async def test_criar_usuario_sucesso():
    repositorio = FakeUsuarioRepository()
    hasher = FakePasswordHasher()
    use_case = CriarUsuarioUseCase(repositorio, hasher)

    resultado = await use_case.executar(
        CriarUsuarioInput(
            nome="João", email="joao@x.com", senha="segredo123", perfil=Perfil.MECANICO
        )
    )

    assert resultado.id == 1
    assert resultado.perfil == Perfil.MECANICO
    assert resultado.ativo is True
    usuario_salvo = await repositorio.buscar_por_id(resultado.id)
    assert usuario_salvo.senha_hash == hasher.hash("segredo123")


async def test_criar_usuario_com_email_ja_cadastrado_levanta_erro():
    repositorio = FakeUsuarioRepository()
    use_case = CriarUsuarioUseCase(repositorio, FakePasswordHasher())
    entrada = CriarUsuarioInput(
        nome="João", email="joao@x.com", senha="segredo123", perfil=Perfil.MECANICO
    )
    await use_case.executar(entrada)

    with pytest.raises(EmailJaCadastradoError):
        await use_case.executar(entrada)
