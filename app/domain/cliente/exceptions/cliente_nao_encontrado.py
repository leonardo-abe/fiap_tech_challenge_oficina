from app.domain.cliente.exceptions.cliente_error import ClienteError


class ClienteNaoEncontradoError(ClienteError):
    def __init__(self, identificador: int | str) -> None:
        super().__init__(f"Cliente não encontrado: {identificador}")
