from app.domain.ordem_servico.exceptions.ordem_servico_error import OrdemServicoError


class VeiculoNaoPertenceAoClienteError(OrdemServicoError):
    def __init__(self, veiculo_id: int, cliente_id: int) -> None:
        super().__init__(f"Veículo {veiculo_id} não pertence ao cliente {cliente_id}")
