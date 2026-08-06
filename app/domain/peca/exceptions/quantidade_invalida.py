from app.domain.peca.exceptions.peca_error import PecaError


class QuantidadeInvalidaError(PecaError):
    def __init__(self, quantidade: int) -> None:
        super().__init__(f"Quantidade deve ser maior que zero: {quantidade}")
