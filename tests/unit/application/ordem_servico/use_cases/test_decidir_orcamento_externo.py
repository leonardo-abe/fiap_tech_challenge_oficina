import pytest

from app.application.ordem_servico.use_cases import (
    DecidirOrcamentoExternoUseCase,
    MudarStatusOrdemServicoUseCase,
)
from app.domain.cliente.entities import Cliente
from app.domain.cliente.value_objects import Documento
from app.domain.ordem_servico.entities import OrdemServico
from app.domain.ordem_servico.exceptions import OrdemServicoNaoEncontradaError
from app.domain.ordem_servico.value_objects import StatusOS
from tests.unit.application.fakes import (
    FakeClienteRepository,
    FakeNotificadorOrcamento,
    FakeOrdemServicoRepository,
    FakePecaRepository,
)

_DOCUMENTO = "11144477735"


async def _preparar(status: StatusOS = StatusOS.AGUARDANDO_APROVACAO):
    cliente_repositorio = FakeClienteRepository()
    cliente = await cliente_repositorio.criar(
        Cliente(
            nome="Maria", documento=Documento(valor=_DOCUMENTO), email="maria@x.com", telefone="1"
        )
    )
    ordem_repositorio = FakeOrdemServicoRepository()
    ordem = await ordem_repositorio.criar(
        OrdemServico(cliente_id=cliente.id, veiculo_id=1, status=status)
    )
    mudar_status_use_case = MudarStatusOrdemServicoUseCase(
        ordem_repositorio, FakePecaRepository(), cliente_repositorio, FakeNotificadorOrcamento()
    )
    use_case = DecidirOrcamentoExternoUseCase(
        ordem_repositorio, cliente_repositorio, mudar_status_use_case
    )
    return use_case, ordem


async def test_aprovar_orcamento_com_documento_correto_transiciona_para_em_execucao():
    use_case, ordem = await _preparar()

    resultado = await use_case.executar(ordem.id, _DOCUMENTO, aprovar=True)

    assert resultado.status == StatusOS.EM_EXECUCAO.value


async def test_reprovar_orcamento_com_documento_correto_transiciona_para_reprovada():
    use_case, ordem = await _preparar()

    resultado = await use_case.executar(ordem.id, _DOCUMENTO, aprovar=False)

    assert resultado.status == StatusOS.REPROVADA.value


async def test_decidir_orcamento_com_documento_errado_levanta_nao_encontrada():
    use_case, ordem = await _preparar()

    with pytest.raises(OrdemServicoNaoEncontradaError):
        await use_case.executar(ordem.id, "52998224725", aprovar=True)


async def test_decidir_orcamento_com_documento_malformado_levanta_nao_encontrada():
    use_case, ordem = await _preparar()

    with pytest.raises(OrdemServicoNaoEncontradaError):
        await use_case.executar(ordem.id, "123", aprovar=True)


async def test_decidir_orcamento_ordem_inexistente_levanta_nao_encontrada():
    use_case, _ = await _preparar()

    with pytest.raises(OrdemServicoNaoEncontradaError):
        await use_case.executar(999, _DOCUMENTO, aprovar=True)


async def test_decidir_orcamento_fora_de_aguardando_aprovacao_levanta_erro():
    from app.domain.ordem_servico.exceptions import TransicaoStatusInvalidaError

    use_case, ordem = await _preparar(status=StatusOS.RECEBIDA)

    with pytest.raises(TransicaoStatusInvalidaError):
        await use_case.executar(ordem.id, _DOCUMENTO, aprovar=True)
