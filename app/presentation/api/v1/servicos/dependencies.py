from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.servico.use_cases import (
    AtualizarServicoUseCase,
    BuscarServicoUseCase,
    CriarServicoUseCase,
    ListarServicosUseCase,
    RemoverServicoUseCase,
)
from app.infrastructure.db.session import get_session
from app.infrastructure.persistence.servico.repository import SQLAlchemyServicoRepository


def get_servico_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyServicoRepository:
    return SQLAlchemyServicoRepository(session=session)


def get_criar_servico_use_case(
    servico_repository: SQLAlchemyServicoRepository = Depends(get_servico_repository),
) -> CriarServicoUseCase:
    return CriarServicoUseCase(servico_repository=servico_repository)


def get_atualizar_servico_use_case(
    servico_repository: SQLAlchemyServicoRepository = Depends(get_servico_repository),
) -> AtualizarServicoUseCase:
    return AtualizarServicoUseCase(servico_repository=servico_repository)


def get_buscar_servico_use_case(
    servico_repository: SQLAlchemyServicoRepository = Depends(get_servico_repository),
) -> BuscarServicoUseCase:
    return BuscarServicoUseCase(servico_repository=servico_repository)


def get_listar_servicos_use_case(
    servico_repository: SQLAlchemyServicoRepository = Depends(get_servico_repository),
) -> ListarServicosUseCase:
    return ListarServicosUseCase(servico_repository=servico_repository)


def get_remover_servico_use_case(
    servico_repository: SQLAlchemyServicoRepository = Depends(get_servico_repository),
) -> RemoverServicoUseCase:
    return RemoverServicoUseCase(servico_repository=servico_repository)
