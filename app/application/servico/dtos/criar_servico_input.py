from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CriarServicoInput:
    nome: str
    descricao: str
    preco: Decimal
