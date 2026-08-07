import pytest

from app.application.ordem_servico.use_cases import MudarStatusOrdemServicoUseCase
from app.domain.ordem_servico.entities import OrdemServico
from app.domain.ordem_servico.exceptions import (
    OrdemServicoNaoEncontradaError,
    TransicaoStatusInvalidaError,
)
from app.domain.ordem_servico.value_objects import StatusOS
from tests.unit.application.fakes import FakeOrdemServicoRepository


async def test_mudar_status_sucesso():
    repositorio = FakeOrdemServicoRepository()
    ordem = await repositorio.criar(OrdemServico(cliente_id=1, veiculo_id=1))
    use_case = MudarStatusOrdemServicoUseCase(repositorio)

    resultado = await use_case.executar(ordem.id, StatusOS.EM_DIAGNOSTICO)

    assert resultado.status == StatusOS.EM_DIAGNOSTICO.value


async def test_mudar_status_ordem_inexistente_levanta_erro():
    use_case = MudarStatusOrdemServicoUseCase(FakeOrdemServicoRepository())

    with pytest.raises(OrdemServicoNaoEncontradaError):
        await use_case.executar(999, StatusOS.EM_DIAGNOSTICO)


async def test_mudar_status_transicao_invalida_levanta_erro():
    repositorio = FakeOrdemServicoRepository()
    ordem = await repositorio.criar(OrdemServico(cliente_id=1, veiculo_id=1))
    use_case = MudarStatusOrdemServicoUseCase(repositorio)

    with pytest.raises(TransicaoStatusInvalidaError):
        await use_case.executar(ordem.id, StatusOS.FINALIZADA)
