import asyncio
import smtplib
from email.message import EmailMessage

from app.application.ordem_servico.dtos import OrdemServicoOutput


class SmtpNotificadorOrcamento:
    """Adapter real: envia o orçamento por e-mail via SMTP (ex.: Gmail com App Password)."""

    def __init__(self, host: str, port: int, usuario: str, senha: str, remetente: str) -> None:
        self._host = host
        self._port = port
        self._usuario = usuario
        self._senha = senha
        self._remetente = remetente

    async def notificar_orcamento_gerado(
        self,
        destinatario_nome: str,
        destinatario_email: str,
        ordem: OrdemServicoOutput,
    ) -> None:
        mensagem = self._montar_mensagem(destinatario_nome, destinatario_email, ordem)
        # smtplib é síncrono/bloqueante - roda em thread separada para não travar o
        # event loop enquanto espera a conexão/handshake com o servidor SMTP.
        await asyncio.to_thread(self._enviar, mensagem)

    def _montar_mensagem(
        self, destinatario_nome: str, destinatario_email: str, ordem: OrdemServicoOutput
    ) -> EmailMessage:
        mensagem = EmailMessage()
        mensagem["Subject"] = f"Orçamento da Ordem de Serviço #{ordem.id} para aprovação"
        mensagem["From"] = self._remetente
        mensagem["To"] = destinatario_email
        mensagem.set_content(self._montar_corpo(destinatario_nome, ordem))
        return mensagem

    def _montar_corpo(self, destinatario_nome: str, ordem: OrdemServicoOutput) -> str:
        linhas = [
            f"Olá, {destinatario_nome}!",
            "",
            f"O orçamento da sua Ordem de Serviço #{ordem.id} está pronto para aprovação:",
            "",
        ]
        for item in ordem.itens_servico:
            linhas.append(f"  Serviço: {item.nome} - R$ {item.valor}")
        for item in ordem.itens_peca:
            linhas.append(f"  Peça: {item.nome} x{item.quantidade} - R$ {item.valor_total}")
        linhas += [
            "",
            f"Total do orçamento: R$ {ordem.orcamento.total}",
            "",
            "Entre em contato com a oficina para aprovar ou recusar este orçamento.",
        ]
        return "\n".join(linhas)

    def _enviar(self, mensagem: EmailMessage) -> None:
        with smtplib.SMTP(self._host, self._port) as smtp:
            smtp.starttls()
            smtp.login(self._usuario, self._senha)
            smtp.send_message(mensagem)
