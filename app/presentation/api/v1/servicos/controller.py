from app.application.servico.dtos import AtualizarServicoInput, CriarServicoInput
from app.application.servico.use_cases import (
    AtualizarServicoUseCase,
    BuscarServicoUseCase,
    CriarServicoUseCase,
    ListarServicosUseCase,
    RemoverServicoUseCase,
)
from app.presentation.api.v1.servicos.schemas import (
    ServicoCreateSchema,
    ServicoSchema,
    ServicoUpdateSchema,
)


class ServicoController:
    def __init__(
        self,
        criar_use_case: CriarServicoUseCase,
        atualizar_use_case: AtualizarServicoUseCase,
        buscar_use_case: BuscarServicoUseCase,
        listar_use_case: ListarServicosUseCase,
        remover_use_case: RemoverServicoUseCase,
    ) -> None:
        self._criar_use_case = criar_use_case
        self._atualizar_use_case = atualizar_use_case
        self._buscar_use_case = buscar_use_case
        self._listar_use_case = listar_use_case
        self._remover_use_case = remover_use_case

    async def criar(self, dados: ServicoCreateSchema) -> ServicoSchema:
        resultado = await self._criar_use_case.executar(
            CriarServicoInput(nome=dados.nome, descricao=dados.descricao, preco=dados.preco)
        )
        return ServicoSchema(**vars(resultado))

    async def listar(self) -> list[ServicoSchema]:
        resultado = await self._listar_use_case.executar()
        return [ServicoSchema(**vars(item)) for item in resultado]

    async def buscar(self, servico_id: int) -> ServicoSchema:
        resultado = await self._buscar_use_case.executar(servico_id)
        return ServicoSchema(**vars(resultado))

    async def atualizar(self, servico_id: int, dados: ServicoUpdateSchema) -> ServicoSchema:
        resultado = await self._atualizar_use_case.executar(
            servico_id,
            AtualizarServicoInput(nome=dados.nome, descricao=dados.descricao, preco=dados.preco),
        )
        return ServicoSchema(**vars(resultado))

    async def remover(self, servico_id: int) -> None:
        await self._remover_use_case.executar(servico_id)
