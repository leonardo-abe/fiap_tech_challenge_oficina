from app.domain.shared.exceptions.dominio_error import DominioError


class ValorMonetarioInvalidoError(DominioError):
    def __init__(self, valor: str) -> None:
        super().__init__(f"Valor monetário inválido: {valor}")
