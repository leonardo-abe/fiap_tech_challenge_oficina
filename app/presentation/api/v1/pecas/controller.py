from app.application.peca.dtos import AtualizarPecaInput, CriarPecaInput, ReporEstoqueInput
from app.application.peca.use_cases import (
    AtualizarPecaUseCase,
    BuscarPecaUseCase,
    CriarPecaUseCase,
    ListarPecasUseCase,
    RemoverPecaUseCase,
    ReporEstoqueUseCase,
)
from app.presentation.api.v1.pecas.schemas import (
    PecaCreateSchema,
    PecaSchema,
    PecaUpdateSchema,
    ReporEstoqueSchema,
)


class PecaController:
    def __init__(
        self,
        criar_use_case: CriarPecaUseCase,
        atualizar_use_case: AtualizarPecaUseCase,
        buscar_use_case: BuscarPecaUseCase,
        listar_use_case: ListarPecasUseCase,
        remover_use_case: RemoverPecaUseCase,
        repor_estoque_use_case: ReporEstoqueUseCase,
    ) -> None:
        self._criar_use_case = criar_use_case
        self._atualizar_use_case = atualizar_use_case
        self._buscar_use_case = buscar_use_case
        self._listar_use_case = listar_use_case
        self._remover_use_case = remover_use_case
        self._repor_estoque_use_case = repor_estoque_use_case

    async def criar(self, dados: PecaCreateSchema) -> PecaSchema:
        resultado = await self._criar_use_case.executar(
            CriarPecaInput(
                nome=dados.nome,
                descricao=dados.descricao,
                preco=dados.preco,
                quantidade_inicial=dados.quantidade_inicial,
            )
        )
        return PecaSchema(**vars(resultado))

    async def listar(
        self, nome: str | None = None, limit: int = 50, offset: int = 0
    ) -> list[PecaSchema]:
        resultado = await self._listar_use_case.executar(nome=nome, limit=limit, offset=offset)
        return [PecaSchema(**vars(item)) for item in resultado]

    async def buscar(self, peca_id: int) -> PecaSchema:
        resultado = await self._buscar_use_case.executar(peca_id)
        return PecaSchema(**vars(resultado))

    async def atualizar(self, peca_id: int, dados: PecaUpdateSchema) -> PecaSchema:
        resultado = await self._atualizar_use_case.executar(
            peca_id,
            AtualizarPecaInput(nome=dados.nome, descricao=dados.descricao, preco=dados.preco),
        )
        return PecaSchema(**vars(resultado))

    async def repor_estoque(self, peca_id: int, dados: ReporEstoqueSchema) -> PecaSchema:
        resultado = await self._repor_estoque_use_case.executar(
            peca_id, ReporEstoqueInput(quantidade=dados.quantidade)
        )
        return PecaSchema(**vars(resultado))

    async def remover(self, peca_id: int) -> None:
        await self._remover_use_case.executar(peca_id)
