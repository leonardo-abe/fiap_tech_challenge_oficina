from app.application.cliente.dtos import AtualizarClienteInput, CriarClienteInput
from app.application.cliente.use_cases import (
    AtualizarClienteUseCase,
    BuscarClienteUseCase,
    CriarClienteUseCase,
    ListarClientesUseCase,
    RemoverClienteUseCase,
)
from app.presentation.api.v1.clientes.schemas import (
    ClienteCreateSchema,
    ClienteSchema,
    ClienteUpdateSchema,
)


class ClienteController:
    def __init__(
        self,
        criar_use_case: CriarClienteUseCase,
        atualizar_use_case: AtualizarClienteUseCase,
        buscar_use_case: BuscarClienteUseCase,
        listar_use_case: ListarClientesUseCase,
        remover_use_case: RemoverClienteUseCase,
    ) -> None:
        self._criar_use_case = criar_use_case
        self._atualizar_use_case = atualizar_use_case
        self._buscar_use_case = buscar_use_case
        self._listar_use_case = listar_use_case
        self._remover_use_case = remover_use_case

    async def criar(self, dados: ClienteCreateSchema) -> ClienteSchema:
        resultado = await self._criar_use_case.executar(
            CriarClienteInput(
                nome=dados.nome,
                documento=dados.documento,
                email=dados.email,
                telefone=dados.telefone,
            )
        )
        return ClienteSchema(**vars(resultado))

    async def listar(self) -> list[ClienteSchema]:
        resultado = await self._listar_use_case.executar()
        return [ClienteSchema(**vars(item)) for item in resultado]

    async def buscar(self, cliente_id: int) -> ClienteSchema:
        resultado = await self._buscar_use_case.executar(cliente_id)
        return ClienteSchema(**vars(resultado))

    async def atualizar(self, cliente_id: int, dados: ClienteUpdateSchema) -> ClienteSchema:
        resultado = await self._atualizar_use_case.executar(
            cliente_id,
            AtualizarClienteInput(
                nome=dados.nome,
                documento=dados.documento,
                email=dados.email,
                telefone=dados.telefone,
            ),
        )
        return ClienteSchema(**vars(resultado))

    async def remover(self, cliente_id: int) -> None:
        await self._remover_use_case.executar(cliente_id)
