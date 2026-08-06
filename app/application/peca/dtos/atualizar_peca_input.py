from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class AtualizarPecaInput:
    nome: str
    descricao: str
    preco: Decimal
