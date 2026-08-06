from fastapi import Depends

from app.application.usuario.use_cases import CriarUsuarioUseCase
from app.presentation.api.v1.auth.dependencies import get_criar_usuario_use_case
from app.presentation.api.v1.usuarios.controller import UsuarioController


def get_usuario_controller(
    criar_use_case: CriarUsuarioUseCase = Depends(get_criar_usuario_use_case),
) -> UsuarioController:
    return UsuarioController(criar_use_case=criar_use_case)
