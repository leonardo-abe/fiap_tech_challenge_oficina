from app.domain.veiculo.exceptions.veiculo_error import VeiculoError


class PlacaInvalidaError(VeiculoError):
    def __init__(self, valor: str) -> None:
        super().__init__(f"Placa inválida: {valor}")
