from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.veiculo.entities import Veiculo
from app.domain.veiculo.value_objects import Placa
from app.infrastructure.persistence.veiculo.models import VeiculoModel


class SQLAlchemyVeiculoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def criar(self, veiculo: Veiculo) -> Veiculo:
        model = VeiculoModel(
            cliente_id=veiculo.cliente_id,
            placa=veiculo.placa.valor,
            marca=veiculo.marca,
            modelo=veiculo.modelo,
            ano=veiculo.ano,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def buscar_por_id(self, veiculo_id: int) -> Veiculo | None:
        model = await self._session.get(VeiculoModel, veiculo_id)
        return self._to_entity(model) if model else None

    async def existe_com_placa(self, placa: str) -> bool:
        resultado = await self._session.execute(
            select(VeiculoModel.id).where(VeiculoModel.placa == placa)
        )
        return resultado.scalar_one_or_none() is not None

    async def listar(self, cliente_id: int | None = None) -> list[Veiculo]:
        query = select(VeiculoModel).order_by(VeiculoModel.id)
        if cliente_id is not None:
            query = query.where(VeiculoModel.cliente_id == cliente_id)
        resultado = await self._session.execute(query)
        return [self._to_entity(model) for model in resultado.scalars().all()]

    async def atualizar(self, veiculo: Veiculo) -> Veiculo:
        model = await self._session.get(VeiculoModel, veiculo.id)
        model.cliente_id = veiculo.cliente_id
        model.placa = veiculo.placa.valor
        model.marca = veiculo.marca
        model.modelo = veiculo.modelo
        model.ano = veiculo.ano
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def remover(self, veiculo_id: int) -> None:
        model = await self._session.get(VeiculoModel, veiculo_id)
        await self._session.delete(model)
        await self._session.flush()

    @staticmethod
    def _to_entity(model: VeiculoModel) -> Veiculo:
        return Veiculo(
            id=model.id,
            cliente_id=model.cliente_id,
            placa=Placa(valor=model.placa),
            marca=model.marca,
            modelo=model.modelo,
            ano=model.ano,
        )
