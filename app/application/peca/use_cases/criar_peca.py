from app.application.peca.dtos import CriarPecaInput, PecaOutput
from app.application.peca.ports import PecaRepositoryProtocol
from app.domain.peca.entities import Peca
from app.domain.shared.value_objects import Money


class CriarPecaUseCase:
    def __init__(self, peca_repository: PecaRepositoryProtocol) -> None:
        self._peca_repository = peca_repository

    async def executar(self, entrada: CriarPecaInput) -> PecaOutput:
        peca = Peca(
            nome=entrada.nome,
            descricao=entrada.descricao,
            preco=Money(valor=entrada.preco),
            quantidade_disponivel=entrada.quantidade_inicial,
        )
        criada = await self._peca_repository.criar(peca)

        return PecaOutput(
            id=criada.id,
            nome=criada.nome,
            descricao=criada.descricao,
            preco=criada.preco.valor,
            quantidade_disponivel=criada.quantidade_disponivel,
        )
