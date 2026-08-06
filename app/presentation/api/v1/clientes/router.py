from fastapi import APIRouter, Depends, status

from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import require_roles
from app.presentation.api.v1.clientes.controller import ClienteController
from app.presentation.api.v1.clientes.dependencies import get_cliente_controller
from app.presentation.api.v1.clientes.schemas import (
    ClienteCreateSchema,
    ClienteSchema,
    ClienteUpdateSchema,
)

router = APIRouter(
    prefix="/api/v1/clientes",
    tags=["clientes"],
    dependencies=[Depends(require_roles(Perfil.ADMIN, Perfil.ATENDENTE))],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_cliente(
    dados: ClienteCreateSchema,
    controller: ClienteController = Depends(get_cliente_controller),
) -> ClienteSchema:
    return await controller.criar(dados)


@router.get("/")
async def listar_clientes(
    controller: ClienteController = Depends(get_cliente_controller),
) -> list[ClienteSchema]:
    return await controller.listar()


@router.get("/{cliente_id}")
async def buscar_cliente(
    cliente_id: int,
    controller: ClienteController = Depends(get_cliente_controller),
) -> ClienteSchema:
    return await controller.buscar(cliente_id)


@router.put("/{cliente_id}")
async def atualizar_cliente(
    cliente_id: int,
    dados: ClienteUpdateSchema,
    controller: ClienteController = Depends(get_cliente_controller),
) -> ClienteSchema:
    return await controller.atualizar(cliente_id, dados)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_cliente(
    cliente_id: int,
    controller: ClienteController = Depends(get_cliente_controller),
) -> None:
    await controller.remover(cliente_id)
