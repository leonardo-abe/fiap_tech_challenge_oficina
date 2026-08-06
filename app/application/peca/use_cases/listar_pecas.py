from app.application.peca.dtos import PecaOutput
from app.application.peca.ports import PecaRepositoryProtocol


class ListarPecasUseCase:
    def __init__(self, peca_repository: PecaRepositoryProtocol) -> None:
        self._peca_repository = peca_repository

    async def executar(self) -> list[PecaOutput]:
        pecas = await self._peca_repository.listar()

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
