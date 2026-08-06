from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.peca.use_cases import (
    AtualizarPecaUseCase,
    BuscarPecaUseCase,
    CriarPecaUseCase,
    ListarPecasUseCase,
    RemoverPecaUseCase,
    ReporEstoqueUseCase,
)
from app.infrastructure.db.session import get_session
from app.infrastructure.persistence.peca.repository import SQLAlchemyPecaRepository


def get_peca_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyPecaRepository:
    return SQLAlchemyPecaRepository(session=session)


def get_criar_peca_use_case(
    peca_repository: SQLAlchemyPecaRepository = Depends(get_peca_repository),
) -> CriarPecaUseCase:
    return CriarPecaUseCase(peca_repository=peca_repository)


def get_atualizar_peca_use_case(
    peca_repository: SQLAlchemyPecaRepository = Depends(get_peca_repository),
) -> AtualizarPecaUseCase:
    return AtualizarPecaUseCase(peca_repository=peca_repository)


def get_buscar_peca_use_case(
    peca_repository: SQLAlchemyPecaRepository = Depends(get_peca_repository),
) -> BuscarPecaUseCase:
    return BuscarPecaUseCase(peca_repository=peca_repository)


def get_listar_pecas_use_case(
    peca_repository: SQLAlchemyPecaRepository = Depends(get_peca_repository),
) -> ListarPecasUseCase:
    return ListarPecasUseCase(peca_repository=peca_repository)


def get_remover_peca_use_case(
    peca_repository: SQLAlchemyPecaRepository = Depends(get_peca_repository),
) -> RemoverPecaUseCase:
    return RemoverPecaUseCase(peca_repository=peca_repository)


def get_repor_estoque_use_case(
    peca_repository: SQLAlchemyPecaRepository = Depends(get_peca_repository),
) -> ReporEstoqueUseCase:
    return ReporEstoqueUseCase(peca_repository=peca_repository)
