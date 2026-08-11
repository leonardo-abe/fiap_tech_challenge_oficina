from app.domain.veiculo.exceptions.veiculo_error import VeiculoError


class VeiculoNaoEncontradoError(VeiculoError):
    def __init__(self, identificador: int | str) -> None:
        super().__init__(f"Veículo não encontrado: {identificador}")
