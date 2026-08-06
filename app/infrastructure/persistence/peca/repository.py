from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.peca.entities import Peca
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
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def buscar_por_id(self, peca_id: int) -> Peca | None:
        model = await self._session.get(PecaModel, peca_id)
        return self._to_entity(model) if model else None

    async def listar(self) -> list[Peca]:
        resultado = await self._session.execute(select(PecaModel).order_by(PecaModel.nome))
        return [self._to_entity(model) for model in resultado.scalars().all()]

    async def atualizar(self, peca: Peca) -> Peca:
        model = await self._session.get(PecaModel, peca.id)
        model.nome = peca.nome
        model.descricao = peca.descricao
        model.preco = peca.preco.valor
        model.quantidade_disponivel = peca.quantidade_disponivel
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def remover(self, peca_id: int) -> None:
        model = await self._session.get(PecaModel, peca_id)
        await self._session.delete(model)
        await self._session.commit()

    @staticmethod
    def _to_entity(model: PecaModel) -> Peca:
        return Peca(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            preco=Money(valor=model.preco),
            quantidade_disponivel=model.quantidade_disponivel,
        )
