import pytest

from app.application.ordem_servico.use_cases import GerarOrcamentoUseCase
from app.domain.cliente.exceptions import ClienteNaoEncontradoError
from app.domain.ordem_servico.entities import OrdemServico
from app.domain.ordem_servico.exceptions import (
    OrdemServicoNaoEncontradaError,
    TransicaoStatusInvalidaError,
)
from app.domain.ordem_servico.value_objects import StatusOS
from tests.unit.application.fakes import (
    FakeClienteRepository,
    FakeNotificadorOrcamento,
    FakeOrdemServicoRepository,
)

from ._fixtures import criar_cliente_padrao


async def test_gerar_orcamento_muda_status_e_notifica_cliente():
    ordem_repo = FakeOrdemServicoRepository()
    cliente_repo = FakeClienteRepository()
    notificador = FakeNotificadorOrcamento()
    cliente = await criar_cliente_padrao(cliente_repo)
    ordem = await ordem_repo.criar(OrdemServico(cliente_id=cliente.id, veiculo_id=1))
    ordem.mudar_status(StatusOS.EM_DIAGNOSTICO)
    use_case = GerarOrcamentoUseCase(
        ordem_servico_repository=ordem_repo,
        cliente_repository=cliente_repo,
        notificador=notificador,
    )

    resultado = await use_case.executar(ordem.id)

    assert resultado.status == StatusOS.AGUARDANDO_APROVACAO.value
    assert notificador.notificacoes_enviadas == [(cliente.nome, cliente.email, ordem.id)]


async def test_gerar_orcamento_ordem_inexistente_levanta_erro():
    use_case = GerarOrcamentoUseCase(
        ordem_servico_repository=FakeOrdemServicoRepository(),
        cliente_repository=FakeClienteRepository(),
        notificador=FakeNotificadorOrcamento(),
    )

    with pytest.raises(OrdemServicoNaoEncontradaError):
        await use_case.executar(999)


async def test_gerar_orcamento_cliente_inexistente_levanta_erro():
    ordem_repo = FakeOrdemServicoRepository()
    ordem = await ordem_repo.criar(OrdemServico(cliente_id=999, veiculo_id=1))
    ordem.mudar_status(StatusOS.EM_DIAGNOSTICO)
    use_case = GerarOrcamentoUseCase(
        ordem_servico_repository=ordem_repo,
        cliente_repository=FakeClienteRepository(),
        notificador=FakeNotificadorOrcamento(),
    )

    with pytest.raises(ClienteNaoEncontradoError):
        await use_case.executar(ordem.id)


async def test_gerar_orcamento_transicao_invalida_levanta_erro_e_nao_notifica():
    ordem_repo = FakeOrdemServicoRepository()
    cliente_repo = FakeClienteRepository()
    notificador = FakeNotificadorOrcamento()
    cliente = await criar_cliente_padrao(cliente_repo)
    ordem = await ordem_repo.criar(OrdemServico(cliente_id=cliente.id, veiculo_id=1))
    use_case = GerarOrcamentoUseCase(
        ordem_servico_repository=ordem_repo,
        cliente_repository=cliente_repo,
        notificador=notificador,
    )

    # ordem ainda em RECEBIDA - só EM_DIAGNOSTICO -> AGUARDANDO_APROVACAO é válido
    with pytest.raises(TransicaoStatusInvalidaError):
        await use_case.executar(ordem.id)

    assert notificador.notificacoes_enviadas == []
