from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PecaOutput:
    id: int
    nome: str
    descricao: str
    preco: Decimal
    quantidade_disponivel: int
