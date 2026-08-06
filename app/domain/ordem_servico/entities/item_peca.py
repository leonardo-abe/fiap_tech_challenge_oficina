from dataclasses import dataclass

from app.domain.ordem_servico.exceptions.quantidade_item_invalida import (
    QuantidadeItemInvalidaError,
)
from app.domain.shared.value_objects import Money


@dataclass
class ItemPeca:
    peca_id: int
    nome: str
    quantidade: int
    valor_unitario: Money
    id: int | None = None

    def __post_init__(self) -> None:
        if self.quantidade <= 0:
            raise QuantidadeItemInvalidaError(self.quantidade)

    @property
    def valor_total(self) -> Money:
        return self.valor_unitario.multiplicar(self.quantidade)
