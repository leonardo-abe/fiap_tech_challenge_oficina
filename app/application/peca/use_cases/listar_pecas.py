from app.application.peca.dtos import PecaOutput
from app.application.peca.ports import PecaRepositoryProtocol


class ListarPecasUseCase:
    def __init__(self, peca_repository: PecaRepositoryProtocol) -> None:
        self._peca_repository = peca_repository

    async def executar(
        self, nome: str | None = None, limit: int = 50, offset: int = 0
    ) -> list[PecaOutput]:
        pecas = await self._peca_repository.listar(nome=nome, limit=limit, offset=offset)

        return [
            PecaOutput(
                id=peca.id,
                nome=peca.nome,
                descricao=peca.descricao,
                preco=peca.preco.valor,
                quantidade_disponivel=peca.quantidade_disponivel,
            )
            for peca in pecas
        ]
