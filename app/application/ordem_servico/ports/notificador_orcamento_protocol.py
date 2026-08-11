from typing import Protocol

from app.application.ordem_servico.dtos import OrdemServicoOutput


class NotificadorOrcamentoProtocol(Protocol):
    async def notificar_orcamento_gerado(
        self,
        destinatario_nome: str,
        destinatario_email: str,
        ordem: OrdemServicoOutput,
    ) -> None: ...
