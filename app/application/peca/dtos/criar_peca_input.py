from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CriarPecaInput:
    nome: str
    descricao: str
    preco: Decimal
    quantidade_inicial: int
