from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal

from app.domain.ordem_servico.entities.item_peca import ItemPeca
from app.domain.ordem_servico.entities.item_servico import ItemServico
from app.domain.ordem_servico.exceptions.ordem_servico_sem_itens import OrdemServicoSemItensError
from app.domain.ordem_servico.exceptions.transicao_status_invalida import (
    TransicaoStatusInvalidaError,
)
from app.domain.ordem_servico.value_objects import Orcamento, StatusOS
from app.domain.shared.value_objects import Money

_TRANSICOES_VALIDAS: dict[StatusOS, frozenset[StatusOS]] = {
    StatusOS.RECEBIDA: frozenset({StatusOS.EM_DIAGNOSTICO, StatusOS.CANCELADA}),
    StatusOS.EM_DIAGNOSTICO: frozenset({StatusOS.AGUARDANDO_APROVACAO, StatusOS.CANCELADA}),
    StatusOS.AGUARDANDO_APROVACAO: frozenset(
        {StatusOS.EM_EXECUCAO, StatusOS.REPROVADA, StatusOS.CANCELADA}
    ),
    StatusOS.EM_EXECUCAO: frozenset({StatusOS.FINALIZADA}),
    StatusOS.FINALIZADA: frozenset({StatusOS.ENTREGUE}),
    StatusOS.ENTREGUE: frozenset(),
    StatusOS.REPROVADA: frozenset(),
    StatusOS.CANCELADA: frozenset(),
}


@dataclass
class OrdemServico:
    cliente_id: int
    veiculo_id: int
    id: int | None = None
    status: StatusOS = StatusOS.RECEBIDA
    itens_servico: list[ItemServico] = field(default_factory=list)
    itens_peca: list[ItemPeca] = field(default_factory=list)
    recebida_em: datetime = field(default_factory=lambda: datetime.now(UTC))
    execucao_iniciada_em: datetime | None = None
    finalizada_em: datetime | None = None

    def adicionar_item_servico(self, item: ItemServico) -> None:
        self.itens_servico.append(item)

    def adicionar_item_peca(self, item: ItemPeca) -> None:
        self.itens_peca.append(item)

    def validar_possui_itens(self) -> None:
        if not self.itens_servico and not self.itens_peca:
            raise OrdemServicoSemItensError

    def mudar_status(self, novo_status: StatusOS) -> None:
        if novo_status not in _TRANSICOES_VALIDAS[self.status]:
            raise TransicaoStatusInvalidaError(self.id, self.status, novo_status)

        self.status = novo_status
        if novo_status == StatusOS.EM_EXECUCAO:
            self.execucao_iniciada_em = datetime.now(UTC)
        elif novo_status == StatusOS.FINALIZADA:
            self.finalizada_em = datetime.now(UTC)

    def calcular_orcamento(self) -> Orcamento:
        total_servicos = Money(valor=Decimal("0.00"))
        for item in self.itens_servico:
            total_servicos = total_servicos.somar(item.valor)

        total_pecas = Money(valor=Decimal("0.00"))
        for item in self.itens_peca:
            total_pecas = total_pecas.somar(item.valor_total)

        return Orcamento(total_servicos=total_servicos, total_pecas=total_pecas)
