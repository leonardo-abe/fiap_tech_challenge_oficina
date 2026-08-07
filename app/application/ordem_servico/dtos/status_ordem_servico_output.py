from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StatusOrdemServicoOutput:
    id: int
    status: str
    recebida_em: datetime
    execucao_iniciada_em: datetime | None
    finalizada_em: datetime | None
