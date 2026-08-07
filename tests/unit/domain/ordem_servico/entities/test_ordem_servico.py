from decimal import Decimal

import pytest

from app.domain.ordem_servico.entities import ItemPeca, ItemServico, OrdemServico
from app.domain.ordem_servico.exceptions import (
    OrdemServicoSemItensError,
    TransicaoStatusInvalidaError,
)
from app.domain.ordem_servico.value_objects import StatusOS
from app.domain.shared.value_objects import Money


def _criar_ordem(status: StatusOS = StatusOS.RECEBIDA) -> OrdemServico:
    return OrdemServico(cliente_id=1, veiculo_id=1, id=1, status=status)


def test_adicionar_item_servico_e_item_peca():
    ordem = _criar_ordem()

    ordem.adicionar_item_servico(
        ItemServico(servico_id=1, nome="Troca de óleo", valor=Money(valor=Decimal("80.00")))
    )
    ordem.adicionar_item_peca(
        ItemPeca(
            peca_id=1, nome="Filtro", quantidade=2, valor_unitario=Money(valor=Decimal("30.00"))
        )
    )

    assert len(ordem.itens_servico) == 1
    assert len(ordem.itens_peca) == 1


def test_validar_possui_itens_sem_itens_levanta_erro():
    ordem = _criar_ordem()

    with pytest.raises(OrdemServicoSemItensError):
        ordem.validar_possui_itens()


def test_validar_possui_itens_com_item_nao_levanta_erro():
    ordem = _criar_ordem()
    ordem.adicionar_item_servico(
        ItemServico(servico_id=1, nome="Troca de óleo", valor=Money(valor=Decimal("80.00")))
    )

    ordem.validar_possui_itens()


def test_calcular_orcamento_soma_servicos_e_pecas():
    ordem = _criar_ordem()
    ordem.adicionar_item_servico(
        ItemServico(servico_id=1, nome="Troca de óleo", valor=Money(valor=Decimal("80.00")))
    )
    ordem.adicionar_item_peca(
        ItemPeca(
            peca_id=1, nome="Filtro", quantidade=2, valor_unitario=Money(valor=Decimal("30.00"))
        )
    )

    orcamento = ordem.calcular_orcamento()

    assert orcamento.total_servicos.valor == Decimal("80.00")
    assert orcamento.total_pecas.valor == Decimal("60.00")
    assert orcamento.total.valor == Decimal("140.00")


def test_calcular_orcamento_sem_itens_e_zero():
    ordem = _criar_ordem()

    orcamento = ordem.calcular_orcamento()

    assert orcamento.total.valor == Decimal("0.00")


@pytest.mark.parametrize(
    "atual,novo",
    [
        (StatusOS.RECEBIDA, StatusOS.EM_DIAGNOSTICO),
        (StatusOS.RECEBIDA, StatusOS.CANCELADA),
        (StatusOS.EM_DIAGNOSTICO, StatusOS.AGUARDANDO_APROVACAO),
        (StatusOS.EM_DIAGNOSTICO, StatusOS.CANCELADA),
        (StatusOS.AGUARDANDO_APROVACAO, StatusOS.EM_EXECUCAO),
        (StatusOS.AGUARDANDO_APROVACAO, StatusOS.REPROVADA),
        (StatusOS.AGUARDANDO_APROVACAO, StatusOS.CANCELADA),
        (StatusOS.EM_EXECUCAO, StatusOS.FINALIZADA),
        (StatusOS.FINALIZADA, StatusOS.ENTREGUE),
    ],
)
def test_mudar_status_transicoes_validas(atual, novo):
    ordem = _criar_ordem(status=atual)

    ordem.mudar_status(novo)

    assert ordem.status == novo


def test_mudar_status_para_em_execucao_marca_execucao_iniciada_em():
    ordem = _criar_ordem(status=StatusOS.AGUARDANDO_APROVACAO)
    assert ordem.execucao_iniciada_em is None

    ordem.mudar_status(StatusOS.EM_EXECUCAO)

    assert ordem.execucao_iniciada_em is not None


def test_mudar_status_para_finalizada_marca_finalizada_em():
    ordem = _criar_ordem(status=StatusOS.EM_EXECUCAO)
    assert ordem.finalizada_em is None

    ordem.mudar_status(StatusOS.FINALIZADA)

    assert ordem.finalizada_em is not None


@pytest.mark.parametrize(
    "atual,novo",
    [
        (StatusOS.RECEBIDA, StatusOS.EM_EXECUCAO),
        (StatusOS.RECEBIDA, StatusOS.RECEBIDA),
        (StatusOS.EM_EXECUCAO, StatusOS.RECEBIDA),
        (StatusOS.FINALIZADA, StatusOS.CANCELADA),
        (StatusOS.ENTREGUE, StatusOS.RECEBIDA),
        (StatusOS.REPROVADA, StatusOS.EM_DIAGNOSTICO),
        (StatusOS.CANCELADA, StatusOS.RECEBIDA),
    ],
)
def test_mudar_status_transicoes_invalidas_levantam_erro(atual, novo):
    ordem = _criar_ordem(status=atual)

    with pytest.raises(TransicaoStatusInvalidaError):
        ordem.mudar_status(novo)

    assert ordem.status == atual
