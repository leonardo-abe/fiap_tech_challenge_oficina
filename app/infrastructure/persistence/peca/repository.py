from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.peca.entities import Peca
from app.domain.peca.exceptions import EstoqueInsuficienteError, PecaNaoEncontradaError
from app.domain.shared.value_objects import Money
from app.infrastructure.persistence.peca.models import PecaModel


class SQLAlchemyPecaRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def criar(self, peca: Peca) -> Peca:
        model = PecaModel(
            nome=peca.nome,
            descricao=peca.descricao,
            preco=peca.preco.valor,
            quantidade_disponivel=peca.quantidade_disponivel,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def buscar_por_id(self, peca_id: int) -> Peca | None:
        model = await self._session.get(PecaModel, peca_id)
        return self._to_entity(model) if model else None

    async def listar(self, nome: str | None = None, limit: int = 50, offset: int = 0) -> list[Peca]:
        query = select(PecaModel).order_by(PecaModel.nome)
        if nome is not None:
            query = query.where(PecaModel.nome.ilike(f"%{nome}%"))
        query = query.limit(limit).offset(offset)
        resultado = await self._session.execute(query)
        return [self._to_entity(model) for model in resultado.scalars().all()]

    async def atualizar(self, peca: Peca) -> Peca:
        # quantidade_disponivel nunca é escrita aqui - estoque só se move através de
        # decrementar_estoque/incrementar_estoque (UPDATE atômico), nunca por um
        # load-mutate-save de campo genérico, que sofreria lost update sob concorrência.
        model = await self._session.get(PecaModel, peca.id)
        model.nome = peca.nome
        model.descricao = peca.descricao
        model.preco = peca.preco.valor
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def remover(self, peca_id: int) -> None:
        model = await self._session.get(PecaModel, peca_id)
        await self._session.delete(model)
        await self._session.flush()

    async def decrementar_estoque(self, peca_id: int, quantidade: int) -> Peca:
        resultado = await self._session.execute(
            update(PecaModel)
            .where(PecaModel.id == peca_id, PecaModel.quantidade_disponivel >= quantidade)
            .values(quantidade_disponivel=PecaModel.quantidade_disponivel - quantidade)
            .returning(PecaModel)
        )
        model = resultado.scalar_one_or_none()
        if model is not None:
            return self._to_entity(model)

        # nenhuma linha casou com a condição - ou a peça não existe, ou o estoque atual
        # (já com o efeito de qualquer decremento concorrente) é insuficiente. Busca de
        # novo para saber qual dos dois e relatar o erro certo.
        atual = await self._session.get(PecaModel, peca_id)
        if atual is None:
            raise PecaNaoEncontradaError(peca_id)
        raise EstoqueInsuficienteError(peca_id, atual.quantidade_disponivel, quantidade)

    async def incrementar_estoque(self, peca_id: int, quantidade: int) -> Peca:
        resultado = await self._session.execute(
            update(PecaModel)
            .where(PecaModel.id == peca_id)
            .values(quantidade_disponivel=PecaModel.quantidade_disponivel + quantidade)
            .returning(PecaModel)
        )
        model = resultado.scalar_one_or_none()
        if model is None:
            raise PecaNaoEncontradaError(peca_id)
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: PecaModel) -> Peca:
        return Peca(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            preco=Money(valor=model.preco),
            quantidade_disponivel=model.quantidade_disponivel,
        )
