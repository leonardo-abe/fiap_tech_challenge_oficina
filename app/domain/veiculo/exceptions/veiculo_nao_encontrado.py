from app.domain.veiculo.exceptions.veiculo_error import VeiculoError


class VeiculoNaoEncontradoError(VeiculoError):
    def __init__(self, veiculo_id: int) -> None:
        super().__init__(f"Veículo não encontrado: {veiculo_id}")
