from app.application.cliente.dtos import ClienteOutput
from app.application.cliente.ports import ClienteRepositoryProtocol


class ListarClientesUseCase:
    def __init__(self, cliente_repository: ClienteRepositoryProtocol) -> None:
        self._cliente_repository = cliente_repository

    async def executar(self) -> list[ClienteOutput]:
        clientes = await self._cliente_repository.listar()

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
