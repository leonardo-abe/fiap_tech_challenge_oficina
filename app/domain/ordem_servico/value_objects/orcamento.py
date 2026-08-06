from dataclasses import dataclass

from app.domain.shared.value_objects import Money


@dataclass(frozen=True)
class Orcamento:
    total_servicos: Money
    total_pecas: Money

    @property
    def total(self) -> Money:
        return self.total_servicos.somar(self.total_pecas)
