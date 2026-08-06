from dataclasses import dataclass


@dataclass(frozen=True)
class ItemPecaInput:
    peca_id: int
    quantidade: int
