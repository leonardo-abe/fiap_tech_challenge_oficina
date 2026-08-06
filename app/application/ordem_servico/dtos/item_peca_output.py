from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ItemPecaOutput:
    peca_id: int
    nome: str
    quantidade: int
    valor_unitario: Decimal
    valor_total: Decimal
