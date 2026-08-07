from app.application.cliente.dtos import CriarClienteInput
from app.application.cliente.use_cases import CriarClienteUseCase, ListarClientesUseCase
from tests.unit.application.fakes import FakeClienteRepository


async def test_listar_clientes_vazio():
    resultado = await ListarClientesUseCase(FakeClienteRepository()).executar()

    assert resultado == []


async def test_listar_clientes_com_registros():
    repositorio = FakeClienteRepository()
    criar_use_case = CriarClienteUseCase(repositorio)
    await criar_use_case.executar(
        CriarClienteInput(
            nome="Maria Silva", documento="11144477735", email="maria@x.com", telefone="1199999"
        )
    )
    await criar_use_case.executar(
        CriarClienteInput(
            nome="João Souza", documento="52998224725", email="joao@x.com", telefone="1188888"
        )
    )

    resultado = await ListarClientesUseCase(repositorio).executar()

    assert len(resultado) == 2
