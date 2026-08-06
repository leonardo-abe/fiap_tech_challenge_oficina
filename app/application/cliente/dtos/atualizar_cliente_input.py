from dataclasses import dataclass


@dataclass(frozen=True)
class AtualizarClienteInput:
    nome: str
    documento: str
    email: str
    telefone: str
