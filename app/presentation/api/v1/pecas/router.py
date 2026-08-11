from fastapi import APIRouter, Depends, Query, status

from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import require_roles
from app.presentation.api.v1.pecas.controller import PecaController
from app.presentation.api.v1.pecas.dependencies import get_peca_controller
from app.presentation.api.v1.pecas.schemas import (
    PecaCreateSchema,
    PecaSchema,
    PecaUpdateSchema,
    ReporEstoqueSchema,
)

router = APIRouter(prefix="/api/v1/pecas", tags=["pecas"])

# Mesmo racional do catálogo de serviços: gestão (criar/editar/remover/repor estoque) é
# só do ADMIN; consulta é liberada a qualquer perfil autenticado (necessário para montar
# orçamento/diagnóstico de uma OS).
_apenas_admin = Depends(require_roles(Perfil.ADMIN))
_qualquer_perfil = Depends(require_roles(Perfil.ADMIN, Perfil.ATENDENTE, Perfil.MECANICO))


@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[_apenas_admin])
async def criar_peca(
    dados: PecaCreateSchema,
    controller: PecaController = Depends(get_peca_controller),
) -> PecaSchema:
    return await controller.criar(dados)


@router.get("/", dependencies=[_qualquer_perfil])
async def listar_pecas(
    nome: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    controller: PecaController = Depends(get_peca_controller),
) -> list[PecaSchema]:
    return await controller.listar(nome=nome, limit=limit, offset=offset)


@router.get("/{peca_id}", dependencies=[_qualquer_perfil])
async def buscar_peca(
    peca_id: int,
    controller: PecaController = Depends(get_peca_controller),
) -> PecaSchema:
    return await controller.buscar(peca_id)


@router.put("/{peca_id}", dependencies=[_apenas_admin])
async def atualizar_peca(
    peca_id: int,
    dados: PecaUpdateSchema,
    controller: PecaController = Depends(get_peca_controller),
) -> PecaSchema:
    return await controller.atualizar(peca_id, dados)


@router.patch("/{peca_id}/estoque", dependencies=[_apenas_admin])
async def repor_estoque(
    peca_id: int,
    dados: ReporEstoqueSchema,
    controller: PecaController = Depends(get_peca_controller),
) -> PecaSchema:
    return await controller.repor_estoque(peca_id, dados)


@router.delete("/{peca_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[_apenas_admin])
async def remover_peca(
    peca_id: int,
    controller: PecaController = Depends(get_peca_controller),
) -> None:
    await controller.remover(peca_id)
