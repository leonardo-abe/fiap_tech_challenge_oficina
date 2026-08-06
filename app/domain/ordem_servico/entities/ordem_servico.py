from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal

from app.domain.ordem_servico.entities.item_peca import ItemPeca
from app.domain.ordem_servico.entities.item_servico import ItemServico
from app.domain.ordem_servico.exceptions.ordem_servico_sem_itens import OrdemServicoSemItensError
from app.domain.ordem_servico.value_objects import Orcamento, StatusOS
from app.domain.shared.value_objects import Money


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

    def calcular_orcamento(self) -> Orcamento:
        total_servicos = Money(valor=Decimal("0.00"))
        for item in self.itens_servico:
            total_servicos = total_servicos.somar(item.valor)

        total_pecas = Money(valor=Decimal("0.00"))
        for item in self.itens_peca:
            total_pecas = total_pecas.somar(item.valor_total)

        return Orcamento(total_servicos=total_servicos, total_pecas=total_pecas)
