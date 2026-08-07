import pytest

from app.application.ordem_servico.use_cases import BuscarOrdemServicoUseCase
from app.domain.ordem_servico.entities import OrdemServico
from app.domain.ordem_servico.exceptions import OrdemServicoNaoEncontradaError
from tests.unit.application.fakes import FakeOrdemServicoRepository


async def test_buscar_ordem_servico_existente():
    repositorio = FakeOrdemServicoRepository()
    criada = await repositorio.criar(OrdemServico(cliente_id=1, veiculo_id=1))

    resultado = await BuscarOrdemServicoUseCase(repositorio).executar(criada.id)

    assert resultado.cliente_id == 1


async def test_buscar_ordem_servico_inexistente_levanta_erro():
    use_case = BuscarOrdemServicoUseCase(FakeOrdemServicoRepository())

    with pytest.raises(OrdemServicoNaoEncontradaError):
        await use_case.executar(999)
