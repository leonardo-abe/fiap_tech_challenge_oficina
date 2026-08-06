from typing import Protocol

from app.domain.ordem_servico.entities import OrdemServico


class OrdemServicoRepositoryProtocol(Protocol):
    async def criar(self, ordem: OrdemServico) -> OrdemServico: ...
