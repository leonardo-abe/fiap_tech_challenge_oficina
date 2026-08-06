from dataclasses import dataclass

from app.domain.shared.value_objects import Money


@dataclass
class ItemServico:
    servico_id: int
    nome: str
    valor: Money
    id: int | None = None
