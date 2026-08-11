from decimal import Decimal

from app.application.peca.dtos import CriarPecaInput
from app.application.peca.use_cases import CriarPecaUseCase, ListarPecasUseCase
from tests.unit.application.fakes import FakePecaRepository


async def test_listar_pecas_vazio():
    resultado = await ListarPecasUseCase(FakePecaRepository()).executar()

    assert resultado == []


async def test_listar_pecas_com_registros():
    repositorio = FakePecaRepository()
    await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Filtro", descricao="Filtro", preco=Decimal("39.90"), quantidade_inicial=10
        )
    )
    await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Vela", descricao="Vela de ignição", preco=Decimal("25.00"), quantidade_inicial=5
        )
    )

    resultado = await ListarPecasUseCase(repositorio).executar()

    assert len(resultado) == 2


async def test_listar_pecas_filtra_por_nome_parcial_case_insensitive():
    repositorio = FakePecaRepository()
    await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Filtro de óleo", descricao="Filtro", preco=Decimal("39.90"), quantidade_inicial=10
        )
    )
    await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Vela", descricao="Vela de ignição", preco=Decimal("25.00"), quantidade_inicial=5
        )
    )

    resultado = await ListarPecasUseCase(repositorio).executar(nome="filtro")

    assert len(resultado) == 1
    assert resultado[0].nome == "Filtro de óleo"


async def test_listar_pecas_respeita_limit_e_offset():
    repositorio = FakePecaRepository()
    await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Filtro", descricao="Filtro", preco=Decimal("39.90"), quantidade_inicial=10
        )
    )
    await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Vela", descricao="Vela de ignição", preco=Decimal("25.00"), quantidade_inicial=5
        )
    )

    primeira_pagina = await ListarPecasUseCase(repositorio).executar(limit=1, offset=0)
    segunda_pagina = await ListarPecasUseCase(repositorio).executar(limit=1, offset=1)

    assert len(primeira_pagina) == 1
    assert len(segunda_pagina) == 1
    assert primeira_pagina[0].id != segunda_pagina[0].id
