from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.veiculo.use_cases import (
    AtualizarVeiculoUseCase,
    BuscarVeiculoUseCase,
    CriarVeiculoUseCase,
    ListarVeiculosUseCase,
    RemoverVeiculoUseCase,
)
from app.infrastructure.db.session import get_session
from app.infrastructure.persistence.cliente.repository import SQLAlchemyClienteRepository
from app.infrastructure.persistence.veiculo.repository import SQLAlchemyVeiculoRepository
from app.presentation.api.v1.clientes.dependencies import get_cliente_repository
from app.presentation.api.v1.veiculos.controller import VeiculoController


def get_veiculo_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyVeiculoRepository:
    return SQLAlchemyVeiculoRepository(session=session)


def get_criar_veiculo_use_case(
    veiculo_repository: SQLAlchemyVeiculoRepository = Depends(get_veiculo_repository),
    cliente_repository: SQLAlchemyClienteRepository = Depends(get_cliente_repository),
) -> CriarVeiculoUseCase:
    return CriarVeiculoUseCase(
        veiculo_repository=veiculo_repository, cliente_repository=cliente_repository
    )


def get_atualizar_veiculo_use_case(
    veiculo_repository: SQLAlchemyVeiculoRepository = Depends(get_veiculo_repository),
    cliente_repository: SQLAlchemyClienteRepository = Depends(get_cliente_repository),
) -> AtualizarVeiculoUseCase:
    return AtualizarVeiculoUseCase(
        veiculo_repository=veiculo_repository, cliente_repository=cliente_repository
    )


def get_buscar_veiculo_use_case(
    veiculo_repository: SQLAlchemyVeiculoRepository = Depends(get_veiculo_repository),
) -> BuscarVeiculoUseCase:
    return BuscarVeiculoUseCase(veiculo_repository=veiculo_repository)


def get_listar_veiculos_use_case(
    veiculo_repository: SQLAlchemyVeiculoRepository = Depends(get_veiculo_repository),
) -> ListarVeiculosUseCase:
    return ListarVeiculosUseCase(veiculo_repository=veiculo_repository)


def get_remover_veiculo_use_case(
    veiculo_repository: SQLAlchemyVeiculoRepository = Depends(get_veiculo_repository),
) -> RemoverVeiculoUseCase:
    return RemoverVeiculoUseCase(veiculo_repository=veiculo_repository)


def get_veiculo_controller(
    criar_use_case: CriarVeiculoUseCase = Depends(get_criar_veiculo_use_case),
    atualizar_use_case: AtualizarVeiculoUseCase = Depends(get_atualizar_veiculo_use_case),
    buscar_use_case: BuscarVeiculoUseCase = Depends(get_buscar_veiculo_use_case),
    listar_use_case: ListarVeiculosUseCase = Depends(get_listar_veiculos_use_case),
    remover_use_case: RemoverVeiculoUseCase = Depends(get_remover_veiculo_use_case),
) -> VeiculoController:
    return VeiculoController(
        criar_use_case=criar_use_case,
        atualizar_use_case=atualizar_use_case,
        buscar_use_case=buscar_use_case,
        listar_use_case=listar_use_case,
        remover_use_case=remover_use_case,
    )
