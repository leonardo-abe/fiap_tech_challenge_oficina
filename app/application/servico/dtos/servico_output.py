from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ServicoOutput:
    id: int
    nome: str
    descricao: str
    preco: Decimal
