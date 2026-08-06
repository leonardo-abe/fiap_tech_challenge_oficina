from app.application.servico.ports import ServicoRepositoryProtocol
from app.domain.servico.exceptions import ServicoNaoEncontradoError


class RemoverServicoUseCase:
    def __init__(self, servico_repository: ServicoRepositoryProtocol) -> None:
        self._servico_repository = servico_repository

    async def executar(self, servico_id: int) -> None:
        servico = await self._servico_repository.buscar_por_id(servico_id)
        if servico is None:
            raise ServicoNaoEncontradoError(servico_id)

        await self._servico_repository.remover(servico_id)
