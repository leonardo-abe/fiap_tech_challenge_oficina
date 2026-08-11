from app.infrastructure.notificacao.log_notificador_orcamento import LogNotificadorOrcamento

from ._fixtures import ordem_output_padrao


async def test_log_notificador_registra_notificacao_sem_lancar_erro(caplog):
    notificador = LogNotificadorOrcamento()
    ordem = ordem_output_padrao()

    with caplog.at_level("INFO"):
        await notificador.notificar_orcamento_gerado(
            destinatario_nome="Maria",
            destinatario_email="maria@x.com",
            ordem=ordem,
        )

    [registro] = caplog.records
    assert "42" in registro.getMessage()
    assert "maria@x.com" in registro.getMessage()
