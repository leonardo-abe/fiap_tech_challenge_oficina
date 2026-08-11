import logging

from app.application.ordem_servico.dtos import OrdemServicoOutput

logger = logging.getLogger(__name__)


class LogNotificadorOrcamento:
    """Adapter padrão/fake: registra a notificação em log em vez de enviar de fato.

    Usado quando NOTIFICACAO_BACKEND=log - útil em desenvolvimento, testes e CI,
    onde não faz sentido depender de um servidor SMTP real disponível.
    """

    async def notificar_orcamento_gerado(
        self,
        destinatario_nome: str,
        destinatario_email: str,
        ordem: OrdemServicoOutput,
    ) -> None:
        logger.info(
            "[notificacao-orcamento] OS #%s - orçamento de R$ %s enviado para %s <%s>",
            ordem.id,
            ordem.orcamento.total,
            destinatario_nome,
            destinatario_email,
        )
