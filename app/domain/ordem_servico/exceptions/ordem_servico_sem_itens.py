from app.domain.ordem_servico.exceptions.ordem_servico_error import OrdemServicoError


class OrdemServicoSemItensError(OrdemServicoError):
    def __init__(self) -> None:
        super().__init__("Uma ordem de serviço precisa de ao menos um item de serviço ou peça")
