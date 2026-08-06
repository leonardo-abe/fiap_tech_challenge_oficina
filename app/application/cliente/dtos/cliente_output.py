from dataclasses import dataclass


@dataclass(frozen=True)
class ClienteOutput:
    id: int
    nome: str
    documento: str
    email: str
    telefone: str
