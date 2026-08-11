from decimal import Decimal

from app.application.servico.dtos import CriarServicoInput
from app.application.servico.use_cases import CriarServicoUseCase, ListarServicosUseCase
from tests.unit.application.fakes import FakeServicoRepository


async def test_listar_servicos_vazio():
    resultado = await ListarServicosUseCase(FakeServicoRepository()).executar()

    assert resultado == []


async def test_listar_servicos_com_registros():
    repositorio = FakeServicoRepository()
    await CriarServicoUseCase(repositorio).executar(
        CriarServicoInput(nome="Troca de óleo", descricao="Óleo", preco=Decimal("120.00"))
    )
    await CriarServicoUseCase(repositorio).executar(
        CriarServicoInput(nome="Alinhamento", descricao="Alinhamento", preco=Decimal("80.00"))
    )

    resultado = await ListarServicosUseCase(repositorio).executar()

    assert len(resultado) == 2


async def test_listar_servicos_filtra_por_nome_parcial_case_insensitive():
    repositorio = FakeServicoRepository()
    await CriarServicoUseCase(repositorio).executar(
        CriarServicoInput(nome="Troca de óleo", descricao="Óleo", preco=Decimal("120.00"))
    )
    await CriarServicoUseCase(repositorio).executar(
        CriarServicoInput(nome="Alinhamento", descricao="Alinhamento", preco=Decimal("80.00"))
    )

    resultado = await ListarServicosUseCase(repositorio).executar(nome="ÓLEO")

    assert len(resultado) == 1
    assert resultado[0].nome == "Troca de óleo"


async def test_listar_servicos_respeita_limit_e_offset():
    repositorio = FakeServicoRepository()
    await CriarServicoUseCase(repositorio).executar(
        CriarServicoInput(nome="Troca de óleo", descricao="Óleo", preco=Decimal("120.00"))
    )
    await CriarServicoUseCase(repositorio).executar(
        CriarServicoInput(nome="Alinhamento", descricao="Alinhamento", preco=Decimal("80.00"))
    )

    primeira_pagina = await ListarServicosUseCase(repositorio).executar(limit=1, offset=0)
    segunda_pagina = await ListarServicosUseCase(repositorio).executar(limit=1, offset=1)

    assert len(primeira_pagina) == 1
    assert len(segunda_pagina) == 1
    assert primeira_pagina[0].id != segunda_pagina[0].id
