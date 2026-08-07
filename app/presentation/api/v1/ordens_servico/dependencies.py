from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ordem_servico.use_cases import (
    CriarOrdemServicoUseCase,
    MudarStatusOrdemServicoUseCase,
)
from app.infrastructure.db.session import get_session
from app.infrastructure.persistence.cliente.repository import SQLAlchemyClienteRepository
from app.infrastructure.persistence.ordem_servico.repository import (
    SQLAlchemyOrdemServicoRepository,
)
from app.infrastructure.persistence.peca.repository import SQLAlchemyPecaRepository
from app.infrastructure.persistence.servico.repository import SQLAlchemyServicoRepository
from app.infrastructure.persistence.veiculo.repository import SQLAlchemyVeiculoRepository
from app.presentation.api.v1.clientes.dependencies import get_cliente_repository
from app.presentation.api.v1.ordens_servico.controller import OrdemServicoController
from app.presentation.api.v1.pecas.dependencies import get_peca_repository
from app.presentation.api.v1.servicos.dependencies import get_servico_repository
from app.presentation.api.v1.veiculos.dependencies import get_veiculo_repository


def get_ordem_servico_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyOrdemServicoRepository:
    return SQLAlchemyOrdemServicoRepository(session=session)


def get_criar_ordem_servico_use_case(
    ordem_servico_repository: SQLAlchemyOrdemServicoRepository = Depends(
        get_ordem_servico_repository
    ),
    cliente_repository: SQLAlchemyClienteRepository = Depends(get_cliente_repository),
    veiculo_repository: SQLAlchemyVeiculoRepository = Depends(get_veiculo_repository),
    servico_repository: SQLAlchemyServicoRepository = Depends(get_servico_repository),
    peca_repository: SQLAlchemyPecaRepository = Depends(get_peca_repository),
) -> CriarOrdemServicoUseCase:
    return CriarOrdemServicoUseCase(
        ordem_servico_repository=ordem_servico_repository,
        cliente_repository=cliente_repository,
        veiculo_repository=veiculo_repository,
        servico_repository=servico_repository,
        peca_repository=peca_repository,
    )


def get_mudar_status_ordem_servico_use_case(
    ordem_servico_repository: SQLAlchemyOrdemServicoRepository = Depends(
        get_ordem_servico_repository
    ),
) -> MudarStatusOrdemServicoUseCase:
    return MudarStatusOrdemServicoUseCase(ordem_servico_repository=ordem_servico_repository)


def get_ordem_servico_controller(
    criar_use_case: CriarOrdemServicoUseCase = Depends(get_criar_ordem_servico_use_case),
    mudar_status_use_case: MudarStatusOrdemServicoUseCase = Depends(
        get_mudar_status_ordem_servico_use_case
    ),
) -> OrdemServicoController:
    return OrdemServicoController(
        criar_use_case=criar_use_case, mudar_status_use_case=mudar_status_use_case
    )
