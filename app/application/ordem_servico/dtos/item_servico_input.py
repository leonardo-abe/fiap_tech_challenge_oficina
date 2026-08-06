from dataclasses import dataclass


@dataclass(frozen=True)
class ItemServicoInput:
    servico_id: int
