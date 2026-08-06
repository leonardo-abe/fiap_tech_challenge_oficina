from fastapi import APIRouter, Depends, status

from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import require_roles
from app.presentation.api.v1.usuarios.controller import UsuarioController
from app.presentation.api.v1.usuarios.dependencies import get_usuario_controller
from app.presentation.api.v1.usuarios.schemas import UsuarioCreateSchema, UsuarioSchema

router = APIRouter(prefix="/api/v1/usuarios", tags=["usuarios"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Perfil.ADMIN))],
)
async def criar_usuario(
    dados: UsuarioCreateSchema,
    controller: UsuarioController = Depends(get_usuario_controller),
) -> UsuarioSchema:
    return await controller.criar(dados)
