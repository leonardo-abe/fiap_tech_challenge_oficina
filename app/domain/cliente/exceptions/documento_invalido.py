from app.domain.cliente.exceptions.cliente_error import ClienteError


class DocumentoInvalidoError(ClienteError):
    def __init__(self, valor: str) -> None:
        super().__init__(f"CPF/CNPJ inválido: {valor}")
