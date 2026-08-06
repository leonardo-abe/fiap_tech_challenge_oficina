from app.domain.cliente.exceptions.cliente_error import ClienteError


class ClienteNaoEncontradoError(ClienteError):
    def __init__(self, cliente_id: int) -> None:
        super().__init__(f"Cliente não encontrado: {cliente_id}")
