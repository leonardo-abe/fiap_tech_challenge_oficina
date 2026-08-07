from app.domain.servico.exceptions import ServicoError, ServicoNaoEncontradoError


def test_servico_nao_encontrado_error_mensagem():
    erro = ServicoNaoEncontradoError(8)

    assert "8" in str(erro)
    assert isinstance(erro, ServicoError)
