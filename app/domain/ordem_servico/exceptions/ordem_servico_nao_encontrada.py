from app.domain.ordem_servico.exceptions.ordem_servico_error import OrdemServicoError


class OrdemServicoNaoEncontradaError(OrdemServicoError):
    def __init__(self, ordem_id: int) -> None:
        super().__init__(f"Ordem de serviço não encontrada: {ordem_id}")
