from dataclasses import dataclass, field
from datetime import datetime

from app.application.ordem_servico.dtos.item_peca_output import ItemPecaOutput
from app.application.ordem_servico.dtos.item_servico_output import ItemServicoOutput
from app.application.ordem_servico.dtos.orcamento_output import OrcamentoOutput


@dataclass(frozen=True)
class OrdemServicoOutput:
    id: int
    cliente_id: int
    veiculo_id: int
    status: str
    orcamento: OrcamentoOutput
    recebida_em: datetime
    itens_servico: list[ItemServicoOutput] = field(default_factory=list)
    itens_peca: list[ItemPecaOutput] = field(default_factory=list)
