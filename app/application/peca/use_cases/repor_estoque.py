from app.application.peca.dtos import PecaOutput, ReporEstoqueInput
from app.application.peca.ports import PecaRepositoryProtocol
from app.domain.peca.exceptions import PecaNaoEncontradaError


class ReporEstoqueUseCase:
    def __init__(self, peca_repository: PecaRepositoryProtocol) -> None:
        self._peca_repository = peca_repository

    async def executar(self, peca_id: int, entrada: ReporEstoqueInput) -> PecaOutput:
        peca = await self._peca_repository.buscar_por_id(peca_id)
        if peca is None:
            raise PecaNaoEncontradaError(peca_id)

        peca.repor_estoque(entrada.quantidade)  # valida quantidade > 0
        atualizada = await self._peca_repository.incrementar_estoque(peca_id, entrada.quantidade)

        return PecaOutput(
            id=atualizada.id,
            nome=atualizada.nome,
            descricao=atualizada.descricao,
            preco=atualizada.preco.valor,
            quantidade_disponivel=atualizada.quantidade_disponivel,
        )
