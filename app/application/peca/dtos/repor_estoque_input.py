from dataclasses import dataclass


@dataclass(frozen=True)
class ReporEstoqueInput:
    quantidade: int
