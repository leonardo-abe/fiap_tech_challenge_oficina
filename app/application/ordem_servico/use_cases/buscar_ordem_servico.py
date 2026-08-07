from app.application.ordem_servico.dtos import OrdemServicoOutput
from app.application.ordem_servico.mappers import ordem_servico_to_output
from app.application.ordem_servico.ports import OrdemServicoRepositoryProtocol
from app.domain.ordem_servico.exceptions import OrdemServicoNaoEncontradaError


class BuscarOrdemServicoUseCase:
    def __init__(self, ordem_servico_repository: OrdemServicoRepositoryProtocol) -> None:
        self._ordem_servico_repository = ordem_servico_repository

    async def executar(self, ordem_id: int) -> OrdemServicoOutput:
        ordem = await self._ordem_servico_repository.buscar_por_id(ordem_id)
        if ordem is None:
            raise OrdemServicoNaoEncontradaError(ordem_id)

        return ordem_servico_to_output(ordem)
