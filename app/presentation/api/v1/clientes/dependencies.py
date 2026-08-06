from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.cliente.use_cases import (
    AtualizarClienteUseCase,
    BuscarClienteUseCase,
    CriarClienteUseCase,
    ListarClientesUseCase,
    RemoverClienteUseCase,
)
from app.infrastructure.db.session import get_session
from app.infrastructure.persistence.cliente.repository import SQLAlchemyClienteRepository


def get_cliente_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyClienteRepository:
    return SQLAlchemyClienteRepository(session=session)


def get_criar_cliente_use_case(
    cliente_repository: SQLAlchemyClienteRepository = Depends(get_cliente_repository),
) -> CriarClienteUseCase:
    return CriarClienteUseCase(cliente_repository=cliente_repository)


def get_atualizar_cliente_use_case(
    cliente_repository: SQLAlchemyClienteRepository = Depends(get_cliente_repository),
) -> AtualizarClienteUseCase:
    return AtualizarClienteUseCase(cliente_repository=cliente_repository)


def get_buscar_cliente_use_case(
    cliente_repository: SQLAlchemyClienteRepository = Depends(get_cliente_repository),
) -> BuscarClienteUseCase:
    return BuscarClienteUseCase(cliente_repository=cliente_repository)


def get_listar_clientes_use_case(
    cliente_repository: SQLAlchemyClienteRepository = Depends(get_cliente_repository),
) -> ListarClientesUseCase:
    return ListarClientesUseCase(cliente_repository=cliente_repository)


def get_remover_cliente_use_case(
    cliente_repository: SQLAlchemyClienteRepository = Depends(get_cliente_repository),
) -> RemoverClienteUseCase:
    return RemoverClienteUseCase(cliente_repository=cliente_repository)
