from dataclasses import dataclass


@dataclass(frozen=True)
class CriarClienteInput:
    nome: str
    documento: str
    email: str
    telefone: str
