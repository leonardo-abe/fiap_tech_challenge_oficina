import pytest

from app.application.cliente.dtos import CriarClienteInput
from app.application.cliente.use_cases import CriarClienteUseCase, RemoverClienteUseCase
from app.domain.cliente.exceptions import ClienteNaoEncontradoError
from tests.unit.application.fakes import FakeClienteRepository


async def test_remover_cliente_sucesso():
    repositorio = FakeClienteRepository()
    criado = await CriarClienteUseCase(repositorio).executar(
        CriarClienteInput(
            nome="Maria", documento="11144477735", email="maria@x.com", telefone="1199999"
        )
    )

    await RemoverClienteUseCase(repositorio).executar(criado.id)

    assert await repositorio.buscar_por_id(criado.id) is None


async def test_remover_cliente_inexistente_levanta_erro():
    use_case = RemoverClienteUseCase(FakeClienteRepository())

    with pytest.raises(ClienteNaoEncontradoError):
        await use_case.executar(999)
