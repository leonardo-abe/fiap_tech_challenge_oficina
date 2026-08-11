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


async def test_listar_clientes_respeita_limit_e_offset():
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

    primeira_pagina = await ListarClientesUseCase(repositorio).executar(limit=1, offset=0)
    segunda_pagina = await ListarClientesUseCase(repositorio).executar(limit=1, offset=1)

    assert len(primeira_pagina) == 1
    assert len(segunda_pagina) == 1
    assert primeira_pagina[0].id != segunda_pagina[0].id
