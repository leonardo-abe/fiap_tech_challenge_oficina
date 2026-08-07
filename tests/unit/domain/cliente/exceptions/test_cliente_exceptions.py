from app.domain.cliente.exceptions import (
    ClienteNaoEncontradoError,
    DocumentoInvalidoError,
    DocumentoJaCadastradoError,
)
from app.domain.cliente.exceptions.cliente_error import ClienteError


def test_cliente_nao_encontrado_error_mensagem():
    erro = ClienteNaoEncontradoError(10)

    assert "10" in str(erro)
    assert isinstance(erro, ClienteError)


def test_documento_invalido_error_mensagem():
    erro = DocumentoInvalidoError("123")

    assert "123" in str(erro)


def test_documento_ja_cadastrado_error_mensagem():
    erro = DocumentoJaCadastradoError("11144477735")

    assert "11144477735" in str(erro)
