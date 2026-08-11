from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.ordem_servico.entities import ItemPeca, ItemServico, OrdemServico
from app.domain.ordem_servico.value_objects import StatusOS
from app.domain.shared.value_objects import Money
from app.infrastructure.persistence.ordem_servico.models import (
    ItemPecaModel,
    ItemServicoModel,
    OrdemServicoModel,
)


class SQLAlchemyOrdemServicoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def criar(self, ordem: OrdemServico) -> OrdemServico:
        model = OrdemServicoModel(
            cliente_id=ordem.cliente_id,
            veiculo_id=ordem.veiculo_id,
            status=ordem.status,
            recebida_em=ordem.recebida_em,
            execucao_iniciada_em=ordem.execucao_iniciada_em,
            finalizada_em=ordem.finalizada_em,
            itens_servico=[
                ItemServicoModel(
                    servico_id=item.servico_id, nome=item.nome, valor=item.valor.valor
                )
                for item in ordem.itens_servico
            ],
            itens_peca=[
                ItemPecaModel(
                    peca_id=item.peca_id,
                    nome=item.nome,
                    quantidade=item.quantidade,
                    valor_unitario=item.valor_unitario.valor,
                )
                for item in ordem.itens_peca
            ],
        )
        self._session.add(model)
        # flush() já popula os ids autoincrementados de model e dos filhos em cascata
        # (via relationship); refresh() aqui expiraria as coleções e o acesso a
        # model.itens_servico/itens_peca faria lazy-load síncrono, que não funciona
        # no motor assíncrono (MissingGreenlet).
        await self._session.flush()
        return self._to_entity(model)

    async def buscar_por_id(self, ordem_id: int) -> OrdemServico | None:
        model = await self._buscar_model_com_itens(ordem_id)
        return self._to_entity(model) if model else None

    async def listar(self, limit: int = 50, offset: int = 0) -> list[OrdemServico]:
        resultado = await self._session.execute(
            select(OrdemServicoModel)
            .options(
                selectinload(OrdemServicoModel.itens_servico),
                selectinload(OrdemServicoModel.itens_peca),
            )
            .order_by(OrdemServicoModel.recebida_em.desc())
            .limit(limit)
            .offset(offset)
        )
        return [self._to_entity(model) for model in resultado.scalars().all()]

    async def atualizar(self, ordem: OrdemServico) -> OrdemServico:
        # busca com os itens já carregados (não usa session.get()) porque o identity map
        # é por referência fraca: o model da consulta anterior pode já ter sido coletado
        # pelo GC, e um session.get() puro traria um model novo sem itens_servico/itens_peca
        # carregados - _to_entity acessando essas coleções lazy dispararia uma query
        # síncrona fora do greenlet do SQLAlchemy async (MissingGreenlet).
        model = await self._buscar_model_com_itens(ordem.id)
        model.status = ordem.status
        model.execucao_iniciada_em = ordem.execucao_iniciada_em
        model.finalizada_em = ordem.finalizada_em
        await self._session.flush()
        return self._to_entity(model)

    async def _buscar_model_com_itens(self, ordem_id: int) -> OrdemServicoModel | None:
        resultado = await self._session.execute(
            select(OrdemServicoModel)
            .options(
                selectinload(OrdemServicoModel.itens_servico),
                selectinload(OrdemServicoModel.itens_peca),
            )
            .where(OrdemServicoModel.id == ordem_id)
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    def _to_entity(model: OrdemServicoModel) -> OrdemServico:
        return OrdemServico(
            id=model.id,
            cliente_id=model.cliente_id,
            veiculo_id=model.veiculo_id,
            status=StatusOS(model.status),
            recebida_em=model.recebida_em,
            execucao_iniciada_em=model.execucao_iniciada_em,
            finalizada_em=model.finalizada_em,
            itens_servico=[
                ItemServico(
                    id=item.id,
                    servico_id=item.servico_id,
                    nome=item.nome,
                    valor=Money(valor=item.valor),
                )
                for item in model.itens_servico
            ],
            itens_peca=[
                ItemPeca(
                    id=item.id,
                    peca_id=item.peca_id,
                    nome=item.nome,
                    quantidade=item.quantidade,
                    valor_unitario=Money(valor=item.valor_unitario),
                )
                for item in model.itens_peca
            ],
        )
