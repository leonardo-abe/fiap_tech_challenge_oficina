from app.application.ordem_servico.dtos import OrdemServicoOutput
from app.application.ordem_servico.mappers import ordem_servico_to_output
from app.application.ordem_servico.ports import OrdemServicoRepositoryProtocol


class ListarOrdensServicoUseCase:
    def __init__(self, ordem_servico_repository: OrdemServicoRepositoryProtocol) -> None:
        self._ordem_servico_repository = ordem_servico_repository

    async def executar(self) -> list[OrdemServicoOutput]:
        ordens = await self._ordem_servico_repository.listar()
        return [ordem_servico_to_output(ordem) for ordem in ordens]
