from dataclasses import dataclass

from app.domain.cliente.value_objects import Documento


@dataclass
class Cliente:
    nome: str
    documento: Documento
    email: str
    telefone: str
    id: int | None = None
