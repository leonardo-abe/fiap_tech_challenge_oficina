from fastapi import APIRouter, Depends, Query, status

from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import require_roles
from app.presentation.api.v1.servicos.controller import ServicoController
from app.presentation.api.v1.servicos.dependencies import get_servico_controller
from app.presentation.api.v1.servicos.schemas import (
    ServicoCreateSchema,
    ServicoSchema,
    ServicoUpdateSchema,
)

router = APIRouter(prefix="/api/v1/servicos", tags=["servicos"])

# Gestão do catálogo (criar/editar/remover) é só do ADMIN; consulta é liberada para
# qualquer perfil autenticado, pois atendente e mecânico precisam ver o catálogo para
# montar orçamento/diagnóstico de uma OS.
_apenas_admin = Depends(require_roles(Perfil.ADMIN))
_qualquer_perfil = Depends(require_roles(Perfil.ADMIN, Perfil.ATENDENTE, Perfil.MECANICO))


@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[_apenas_admin])
async def criar_servico(
    dados: ServicoCreateSchema,
    controller: ServicoController = Depends(get_servico_controller),
) -> ServicoSchema:
    return await controller.criar(dados)


@router.get("/", dependencies=[_qualquer_perfil])
async def listar_servicos(
    nome: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    controller: ServicoController = Depends(get_servico_controller),
) -> list[ServicoSchema]:
    return await controller.listar(nome=nome, limit=limit, offset=offset)


@router.get("/{servico_id}", dependencies=[_qualquer_perfil])
async def buscar_servico(
    servico_id: int,
    controller: ServicoController = Depends(get_servico_controller),
) -> ServicoSchema:
    return await controller.buscar(servico_id)


@router.put("/{servico_id}", dependencies=[_apenas_admin])
async def atualizar_servico(
    servico_id: int,
    dados: ServicoUpdateSchema,
    controller: ServicoController = Depends(get_servico_controller),
) -> ServicoSchema:
    return await controller.atualizar(servico_id, dados)


@router.delete(
    "/{servico_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[_apenas_admin]
)
async def remover_servico(
    servico_id: int,
    controller: ServicoController = Depends(get_servico_controller),
) -> None:
    await controller.remover(servico_id)
