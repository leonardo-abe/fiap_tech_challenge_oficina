from app.application.peca.dtos import PecaOutput
from app.application.peca.ports import PecaRepositoryProtocol
from app.domain.peca.exceptions import PecaNaoEncontradaError


class BuscarPecaUseCase:
    def __init__(self, peca_repository: PecaRepositoryProtocol) -> None:
        self._peca_repository = peca_repository

    async def executar(self, peca_id: int) -> PecaOutput:
        peca = await self._peca_repository.buscar_por_id(peca_id)
        if peca is None:
            raise PecaNaoEncontradaError(peca_id)

        return PecaOutput(
            id=peca.id,
            nome=peca.nome,
            descricao=peca.descricao,
            preco=peca.preco.valor,
            quantidade_disponivel=peca.quantidade_disponivel,
        )
