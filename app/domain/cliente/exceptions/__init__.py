from app.domain.cliente.exceptions.cliente_error import ClienteError
from app.domain.cliente.exceptions.cliente_nao_encontrado import ClienteNaoEncontradoError
from app.domain.cliente.exceptions.documento_invalido import DocumentoInvalidoError
from app.domain.cliente.exceptions.documento_ja_cadastrado import DocumentoJaCadastradoError

__all__ = [
    "ClienteError",
    "ClienteNaoEncontradoError",
    "DocumentoInvalidoError",
    "DocumentoJaCadastradoError",
]
