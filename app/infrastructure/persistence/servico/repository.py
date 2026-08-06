from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.servico.entities import Servico
from app.domain.shared.value_objects import Money
from app.infrastructure.persistence.servico.models import ServicoModel


class SQLAlchemyServicoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def criar(self, servico: Servico) -> Servico:
        model = ServicoModel(
            nome=servico.nome, descricao=servico.descricao, preco=servico.preco.valor
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def buscar_por_id(self, servico_id: int) -> Servico | None:
        model = await self._session.get(ServicoModel, servico_id)
        return self._to_entity(model) if model else None

    async def listar(self) -> list[Servico]:
        resultado = await self._session.execute(select(ServicoModel).order_by(ServicoModel.nome))
        return [self._to_entity(model) for model in resultado.scalars().all()]

    async def atualizar(self, servico: Servico) -> Servico:
        model = await self._session.get(ServicoModel, servico.id)
        model.nome = servico.nome
        model.descricao = servico.descricao
        model.preco = servico.preco.valor
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def remover(self, servico_id: int) -> None:
        model = await self._session.get(ServicoModel, servico_id)
        await self._session.delete(model)
        await self._session.flush()

    @staticmethod
    def _to_entity(model: ServicoModel) -> Servico:
        return Servico(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            preco=Money(valor=model.preco),
        )
