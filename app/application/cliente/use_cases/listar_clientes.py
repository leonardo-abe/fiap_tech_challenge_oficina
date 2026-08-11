from app.application.cliente.dtos import ClienteOutput
from app.application.cliente.ports import ClienteRepositoryProtocol


class ListarClientesUseCase:
    def __init__(self, cliente_repository: ClienteRepositoryProtocol) -> None:
        self._cliente_repository = cliente_repository

    async def executar(self, limit: int = 50, offset: int = 0) -> list[ClienteOutput]:
        clientes = await self._cliente_repository.listar(limit=limit, offset=offset)

        return [
            ClienteOutput(
                id=cliente.id,
                nome=cliente.nome,
                documento=cliente.documento.valor,
                email=cliente.email,
                telefone=cliente.telefone,
            )
            for cliente in clientes
        ]
