from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cliente.entities import Cliente
from app.domain.cliente.value_objects import Documento
from app.infrastructure.persistence.cliente.models import ClienteModel


class SQLAlchemyClienteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def criar(self, cliente: Cliente) -> Cliente:
        model = ClienteModel(
            nome=cliente.nome,
            documento=cliente.documento.valor,
            email=cliente.email,
            telefone=cliente.telefone,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        model = await self._session.get(ClienteModel, cliente_id)
        return self._to_entity(model) if model else None

    async def existe_com_documento(self, documento: str) -> bool:
        resultado = await self._session.execute(
            select(ClienteModel.id).where(ClienteModel.documento == documento)
        )
        return resultado.scalar_one_or_none() is not None

    async def listar(self) -> list[Cliente]:
        resultado = await self._session.execute(select(ClienteModel).order_by(ClienteModel.nome))
        return [self._to_entity(model) for model in resultado.scalars().all()]

    async def atualizar(self, cliente: Cliente) -> Cliente:
        model = await self._session.get(ClienteModel, cliente.id)
        model.nome = cliente.nome
        model.documento = cliente.documento.valor
        model.email = cliente.email
        model.telefone = cliente.telefone
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def remover(self, cliente_id: int) -> None:
        model = await self._session.get(ClienteModel, cliente_id)
        await self._session.delete(model)
        await self._session.flush()

    @staticmethod
    def _to_entity(model: ClienteModel) -> Cliente:
        return Cliente(
            id=model.id,
            nome=model.nome,
            documento=Documento(valor=model.documento),
            email=model.email,
            telefone=model.telefone,
        )
