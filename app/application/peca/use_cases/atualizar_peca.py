from app.application.peca.dtos import AtualizarPecaInput, PecaOutput
from app.application.peca.ports import PecaRepositoryProtocol
from app.domain.peca.exceptions import PecaNaoEncontradaError
from app.domain.shared.value_objects import Money


class AtualizarPecaUseCase:
    def __init__(self, peca_repository: PecaRepositoryProtocol) -> None:
        self._peca_repository = peca_repository

    async def executar(self, peca_id: int, entrada: AtualizarPecaInput) -> PecaOutput:
        peca = await self._peca_repository.buscar_por_id(peca_id)
        if peca is None:
            raise PecaNaoEncontradaError(peca_id)

        peca.nome = entrada.nome
        peca.descricao = entrada.descricao
        peca.preco = Money(valor=entrada.preco)
        atualizada = await self._peca_repository.atualizar(peca)

        return PecaOutput(
            id=atualizada.id,
            nome=atualizada.nome,
            descricao=atualizada.descricao,
            preco=atualizada.preco.valor,
            quantidade_disponivel=atualizada.quantidade_disponivel,
        )
