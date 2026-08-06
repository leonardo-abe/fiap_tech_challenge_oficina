from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class AtualizarServicoInput:
    nome: str
    descricao: str
    preco: Decimal
