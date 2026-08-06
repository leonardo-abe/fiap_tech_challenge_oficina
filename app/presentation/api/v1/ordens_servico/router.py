from fastapi import APIRouter, Depends, status

from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import require_roles
from app.presentation.api.v1.ordens_servico.controller import OrdemServicoController
from app.presentation.api.v1.ordens_servico.dependencies import get_ordem_servico_controller
from app.presentation.api.v1.ordens_servico.schemas import (
    OrdemServicoCreateSchema,
    OrdemServicoSchema,
)

router = APIRouter(
    prefix="/api/v1/ordens-servico",
    tags=["ordens-servico"],
    dependencies=[Depends(require_roles(Perfil.ADMIN, Perfil.ATENDENTE))],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_ordem_servico(
    dados: OrdemServicoCreateSchema,
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> OrdemServicoSchema:
    return await controller.criar(dados)
