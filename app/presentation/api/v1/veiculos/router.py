from fastapi import APIRouter, Depends, Query, status

from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import require_roles
from app.presentation.api.v1.veiculos.controller import VeiculoController
from app.presentation.api.v1.veiculos.dependencies import get_veiculo_controller
from app.presentation.api.v1.veiculos.schemas import (
    VeiculoCreateSchema,
    VeiculoSchema,
    VeiculoUpdateSchema,
)

router = APIRouter(
    prefix="/api/v1/veiculos",
    tags=["veiculos"],
    dependencies=[Depends(require_roles(Perfil.ADMIN, Perfil.ATENDENTE))],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_veiculo(
    dados: VeiculoCreateSchema,
    controller: VeiculoController = Depends(get_veiculo_controller),
) -> VeiculoSchema:
    return await controller.criar(dados)


@router.get("/")
async def listar_veiculos(
    cliente_id: int | None = Query(default=None),
    controller: VeiculoController = Depends(get_veiculo_controller),
) -> list[VeiculoSchema]:
    return await controller.listar(cliente_id=cliente_id)


@router.get("/{veiculo_id}")
async def buscar_veiculo(
    veiculo_id: int,
    controller: VeiculoController = Depends(get_veiculo_controller),
) -> VeiculoSchema:
    return await controller.buscar(veiculo_id)


@router.put("/{veiculo_id}")
async def atualizar_veiculo(
    veiculo_id: int,
    dados: VeiculoUpdateSchema,
    controller: VeiculoController = Depends(get_veiculo_controller),
) -> VeiculoSchema:
    return await controller.atualizar(veiculo_id, dados)


@router.delete("/{veiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_veiculo(
    veiculo_id: int,
    controller: VeiculoController = Depends(get_veiculo_controller),
) -> None:
    await controller.remover(veiculo_id)
