from app.domain.ordem_servico.exceptions.ordem_servico_error import OrdemServicoError
from app.domain.ordem_servico.value_objects.status_os import StatusOS


class TransicaoStatusInvalidaError(OrdemServicoError):
    def __init__(self, ordem_id: int | None, atual: StatusOS, novo: StatusOS) -> None:
        super().__init__(
            f"Ordem de serviço {ordem_id}: transição de {atual.value} para {novo.value} "
            "não é permitida"
        )
