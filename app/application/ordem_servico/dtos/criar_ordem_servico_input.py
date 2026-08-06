from dataclasses import dataclass, field

from app.application.ordem_servico.dtos.item_peca_input import ItemPecaInput
from app.application.ordem_servico.dtos.item_servico_input import ItemServicoInput


@dataclass(frozen=True)
class CriarOrdemServicoInput:
    cliente_id: int
    veiculo_id: int
    itens_servico: list[ItemServicoInput] = field(default_factory=list)
    itens_peca: list[ItemPecaInput] = field(default_factory=list)
