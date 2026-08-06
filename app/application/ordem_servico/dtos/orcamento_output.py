from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class OrcamentoOutput:
    total_servicos: Decimal
    total_pecas: Decimal
    total: Decimal
