from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ItemServicoOutput:
    servico_id: int
    nome: str
    valor: Decimal
