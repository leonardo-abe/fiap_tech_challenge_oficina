import pytest

from app.application.cliente.dtos import CriarClienteInput
from app.application.cliente.use_cases import BuscarClienteUseCase, CriarClienteUseCase
from app.domain.cliente.exceptions import ClienteNaoEncontradoError
from tests.unit.application.fakes import FakeClienteRepository


async def test_buscar_cliente_existente():
    repositorio = FakeClienteRepository()
    criado = await CriarClienteUseCase(repositorio).executar(
        CriarClienteInput(
            nome="Maria Silva",
            documento="11144477735",
            email="maria@example.com",
            telefone="11999998888",
        )
    )

    resultado = await BuscarClienteUseCase(repositorio).executar(criado.id)

    assert resultado.nome == "Maria Silva"


async def test_buscar_cliente_inexistente_levanta_erro():
    use_case = BuscarClienteUseCase(FakeClienteRepository())

    with pytest.raises(ClienteNaoEncontradoError):
        await use_case.executar(999)
