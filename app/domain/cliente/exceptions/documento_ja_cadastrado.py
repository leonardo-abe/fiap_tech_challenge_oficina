from app.domain.cliente.exceptions.cliente_error import ClienteError


class DocumentoJaCadastradoError(ClienteError):
    def __init__(self, valor: str) -> None:
        super().__init__(f"Já existe um cliente com o documento: {valor}")
