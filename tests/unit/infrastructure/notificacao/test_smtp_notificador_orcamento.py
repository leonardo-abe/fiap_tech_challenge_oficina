from unittest.mock import MagicMock, patch

from app.infrastructure.notificacao.smtp_notificador_orcamento import SmtpNotificadorOrcamento

from ._fixtures import ordem_output_padrao


def _montar_notificador() -> SmtpNotificadorOrcamento:
    return SmtpNotificadorOrcamento(
        host="smtp.gmail.com",
        port=587,
        usuario="oficina@gmail.com",
        senha="app-password",
        remetente="oficina@gmail.com",
    )


async def test_smtp_notificador_envia_mensagem_com_starttls_e_login():
    notificador = _montar_notificador()
    ordem = ordem_output_padrao()
    smtp_mock = MagicMock()
    smtp_mock.__enter__.return_value = smtp_mock

    with patch("smtplib.SMTP", return_value=smtp_mock) as smtp_cls:
        await notificador.notificar_orcamento_gerado(
            destinatario_nome="Maria",
            destinatario_email="maria@x.com",
            ordem=ordem,
        )

    smtp_cls.assert_called_once_with("smtp.gmail.com", 587)
    smtp_mock.starttls.assert_called_once()
    smtp_mock.login.assert_called_once_with("oficina@gmail.com", "app-password")
    smtp_mock.send_message.assert_called_once()

    mensagem_enviada = smtp_mock.send_message.call_args[0][0]
    assert mensagem_enviada["To"] == "maria@x.com"
    assert mensagem_enviada["From"] == "oficina@gmail.com"
    assert "42" in mensagem_enviada["Subject"]
    corpo = mensagem_enviada.get_content()
    assert "Maria" in corpo
    assert "Troca de óleo" in corpo
    assert "140.00" in corpo
