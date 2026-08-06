from app.domain.ordem_servico.exceptions.ordem_servico_error import OrdemServicoError


class QuantidadeItemInvalidaError(OrdemServicoError):
    def __init__(self, quantidade: int) -> None:
        super().__init__(f"Quantidade do item deve ser maior que zero: {quantidade}")
