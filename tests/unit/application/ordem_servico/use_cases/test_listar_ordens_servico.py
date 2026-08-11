from app.application.ordem_servico.use_cases import ListarOrdensServicoUseCase
from app.domain.ordem_servico.entities import OrdemServico
from tests.unit.application.fakes import FakeOrdemServicoRepository


async def test_listar_ordens_servico_vazio():
    resultado = await ListarOrdensServicoUseCase(FakeOrdemServicoRepository()).executar()

    assert resultado == []


async def test_listar_ordens_servico_com_registros():
    repositorio = FakeOrdemServicoRepository()
    await repositorio.criar(OrdemServico(cliente_id=1, veiculo_id=1))
    await repositorio.criar(OrdemServico(cliente_id=2, veiculo_id=2))

    resultado = await ListarOrdensServicoUseCase(repositorio).executar()

    assert len(resultado) == 2


async def test_listar_ordens_servico_respeita_limit_e_offset():
    repositorio = FakeOrdemServicoRepository()
    await repositorio.criar(OrdemServico(cliente_id=1, veiculo_id=1))
    await repositorio.criar(OrdemServico(cliente_id=2, veiculo_id=2))

    primeira_pagina = await ListarOrdensServicoUseCase(repositorio).executar(limit=1, offset=0)
    segunda_pagina = await ListarOrdensServicoUseCase(repositorio).executar(limit=1, offset=1)

    assert len(primeira_pagina) == 1
    assert len(segunda_pagina) == 1
    assert primeira_pagina[0].id != segunda_pagina[0].id
