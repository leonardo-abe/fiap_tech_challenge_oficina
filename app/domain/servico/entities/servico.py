from dataclasses import dataclass

from app.domain.shared.value_objects import Money


@dataclass
class Servico:
    nome: str
    descricao: str
    preco: Money
    id: int | None = None
