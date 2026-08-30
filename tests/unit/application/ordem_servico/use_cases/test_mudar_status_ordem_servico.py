from decimal import Decimal

import pytest

from app.application.ordem_servico.use_cases import MudarStatusOrdemServicoUseCase
from app.domain.ordem_servico.entities import ItemPeca, OrdemServico
from app.domain.ordem_servico.exceptions import (
    OrdemServicoNaoEncontradaError,
    TransicaoStatusInvalidaError,
)
from app.domain.ordem_servico.value_objects import StatusOS
from app.domain.peca.entities import Peca
from app.domain.shared.value_objects import Money
from tests.unit.application.fakes import FakeOrdemServicoRepository, FakePecaRepository


async def test_mudar_status_sucesso():
    repositorio = FakeOrdemServicoRepository()
    ordem = await repositorio.criar(OrdemServico(cliente_id=1, veiculo_id=1))
    use_case = MudarStatusOrdemServicoUseCase(repositorio, FakePecaRepository())

    resultado = await use_case.executar(ordem.id, StatusOS.EM_DIAGNOSTICO)

    assert resultado.status == StatusOS.EM_DIAGNOSTICO.value


async def test_mudar_status_ordem_inexistente_levanta_erro():
    use_case = MudarStatusOrdemServicoUseCase(FakeOrdemServicoRepository(), FakePecaRepository())

    with pytest.raises(OrdemServicoNaoEncontradaError):
        await use_case.executar(999, StatusOS.EM_DIAGNOSTICO)


async def test_mudar_status_transicao_invalida_levanta_erro():
    repositorio = FakeOrdemServicoRepository()
    ordem = await repositorio.criar(OrdemServico(cliente_id=1, veiculo_id=1))
    use_case = MudarStatusOrdemServicoUseCase(repositorio, FakePecaRepository())

    with pytest.raises(TransicaoStatusInvalidaError):
        await use_case.executar(ordem.id, StatusOS.FINALIZADA)


async def _criar_ordem_com_peca_reservada(peca_repositorio, ordem_repositorio, status: StatusOS):
    peca = await peca_repositorio.criar(
        Peca(
            nome="Filtro de óleo",
            descricao="",
            preco=Money(valor=Decimal("30.00")),
            quantidade_disponivel=2,
        )
    )
    ordem = OrdemServico(cliente_id=1, veiculo_id=1, status=status)
    ordem.adicionar_item_peca(
        ItemPeca(peca_id=peca.id, nome=peca.nome, quantidade=3, valor_unitario=peca.preco)
    )
    ordem = await ordem_repositorio.criar(ordem)
    return ordem, peca


async def test_mudar_status_para_reprovada_estorna_estoque_das_pecas():
    ordem_repositorio = FakeOrdemServicoRepository()
    peca_repositorio = FakePecaRepository()
    ordem, peca = await _criar_ordem_com_peca_reservada(
        peca_repositorio, ordem_repositorio, StatusOS.AGUARDANDO_APROVACAO
    )
    use_case = MudarStatusOrdemServicoUseCase(ordem_repositorio, peca_repositorio)

    resultado = await use_case.executar(ordem.id, StatusOS.REPROVADA)

    assert resultado.status == StatusOS.REPROVADA.value
    peca_atualizada = await peca_repositorio.buscar_por_id(peca.id)
    assert peca_atualizada.quantidade_disponivel == 5


async def test_mudar_status_para_cancelada_estorna_estoque_das_pecas():
    ordem_repositorio = FakeOrdemServicoRepository()
    peca_repositorio = FakePecaRepository()
    ordem, peca = await _criar_ordem_com_peca_reservada(
        peca_repositorio, ordem_repositorio, StatusOS.EM_DIAGNOSTICO
    )
    use_case = MudarStatusOrdemServicoUseCase(ordem_repositorio, peca_repositorio)

    resultado = await use_case.executar(ordem.id, StatusOS.CANCELADA)

    assert resultado.status == StatusOS.CANCELADA.value
    peca_atualizada = await peca_repositorio.buscar_por_id(peca.id)
    assert peca_atualizada.quantidade_disponivel == 5


async def test_mudar_status_para_em_execucao_nao_mexe_no_estoque():
    ordem_repositorio = FakeOrdemServicoRepository()
    peca_repositorio = FakePecaRepository()
    ordem, peca = await _criar_ordem_com_peca_reservada(
        peca_repositorio, ordem_repositorio, StatusOS.AGUARDANDO_APROVACAO
    )
    use_case = MudarStatusOrdemServicoUseCase(ordem_repositorio, peca_repositorio)

    resultado = await use_case.executar(ordem.id, StatusOS.EM_EXECUCAO)

    assert resultado.status == StatusOS.EM_EXECUCAO.value
    peca_atualizada = await peca_repositorio.buscar_por_id(peca.id)
    assert peca_atualizada.quantidade_disponivel == 2
