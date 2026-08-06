from app.application.cliente.ports import ClienteRepositoryProtocol
from app.domain.cliente.exceptions import ClienteNaoEncontradoError


class RemoverClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepositoryProtocol) -> None:
        self._cliente_repository = cliente_repository

    async def executar(self, cliente_id: int) -> None:
        cliente = await self._cliente_repository.buscar_por_id(cliente_id)
        if cliente is None:
            raise ClienteNaoEncontradoError(cliente_id)

        await self._cliente_repository.remover(cliente_id)
