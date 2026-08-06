from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.cliente.exceptions import (
    ClienteNaoEncontradoError,
    DocumentoInvalidoError,
    DocumentoJaCadastradoError,
)
from app.domain.servico.exceptions import ServicoNaoEncontradoError
from app.domain.usuario.exceptions import (
    CredenciaisInvalidasError,
    EmailJaCadastradoError,
    TokenInvalidoError,
)
from app.domain.veiculo.exceptions import (
    PlacaInvalidaError,
    PlacaJaCadastradaError,
    VeiculoNaoEncontradoError,
)


def registrar_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(PlacaInvalidaError)
    async def _placa_invalida(request: Request, exc: PlacaInvalidaError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(exc)}
        )

    @app.exception_handler(PlacaJaCadastradaError)
    async def _placa_ja_cadastrada(request: Request, exc: PlacaJaCadastradaError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

    @app.exception_handler(VeiculoNaoEncontradoError)
    async def _veiculo_nao_encontrado(
        request: Request, exc: VeiculoNaoEncontradoError
    ) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(DocumentoInvalidoError)
    async def _documento_invalido(request: Request, exc: DocumentoInvalidoError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(exc)}
        )

    @app.exception_handler(DocumentoJaCadastradoError)
    async def _documento_ja_cadastrado(
        request: Request, exc: DocumentoJaCadastradoError
    ) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

    @app.exception_handler(ClienteNaoEncontradoError)
    async def _cliente_nao_encontrado(
        request: Request, exc: ClienteNaoEncontradoError
    ) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(ServicoNaoEncontradoError)
    async def _servico_nao_encontrado(
        request: Request, exc: ServicoNaoEncontradoError
    ) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(CredenciaisInvalidasError)
    async def _credenciais_invalidas(
        request: Request, exc: CredenciaisInvalidasError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "E-mail ou senha inválidos."},
        )

    @app.exception_handler(EmailJaCadastradoError)
    async def _email_ja_cadastrado(request: Request, exc: EmailJaCadastradoError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Já existe um usuário com este e-mail."},
        )

    @app.exception_handler(TokenInvalidoError)
    async def _token_invalido(request: Request, exc: TokenInvalidoError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token inválido ou expirado."},
            headers={"WWW-Authenticate": "Bearer"},
        )
