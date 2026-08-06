from app.application.peca.ports import PecaRepositoryProtocol
from app.domain.peca.exceptions import PecaNaoEncontradaError


class RemoverPecaUseCase:
    def __init__(self, peca_repository: PecaRepositoryProtocol) -> None:
        self._peca_repository = peca_repository

    async def executar(self, peca_id: int) -> None:
        peca = await self._peca_repository.buscar_por_id(peca_id)
        if peca is None:
            raise PecaNaoEncontradaError(peca_id)

        await self._peca_repository.remover(peca_id)
