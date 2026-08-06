from app.domain.veiculo.exceptions.veiculo_error import VeiculoError


class PlacaJaCadastradaError(VeiculoError):
    def __init__(self, valor: str) -> None:
        super().__init__(f"Já existe um veículo com a placa: {valor}")
