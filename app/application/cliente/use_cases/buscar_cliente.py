from app.application.cliente.dtos import ClienteOutput
from app.application.cliente.ports import ClienteRepositoryProtocol
from app.domain.cliente.exceptions import ClienteNaoEncontradoError


class BuscarClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepositoryProtocol) -> None:
        self._cliente_repository = cliente_repository

    async def executar(self, cliente_id: int) -> ClienteOutput:
        cliente = await self._cliente_repository.buscar_por_id(cliente_id)
        if cliente is None:
            raise ClienteNaoEncontradoError(cliente_id)

        return ClienteOutput(
            id=cliente.id,
            nome=cliente.nome,
            documento=cliente.documento.valor,
            email=cliente.email,
            telefone=cliente.telefone,
        )
