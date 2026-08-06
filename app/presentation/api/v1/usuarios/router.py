from fastapi import APIRouter, Depends, status

from app.application.usuario.dtos import CriarUsuarioInput
from app.application.usuario.use_cases import CriarUsuarioUseCase
from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import get_criar_usuario_use_case, require_roles
from app.presentation.api.v1.usuarios.schemas import UsuarioCreateSchema, UsuarioSchema

router = APIRouter(prefix="/api/v1/usuarios", tags=["usuarios"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Perfil.ADMIN))],
)
async def criar_usuario(
    dados: UsuarioCreateSchema,
    use_case: CriarUsuarioUseCase = Depends(get_criar_usuario_use_case),
) -> UsuarioSchema:
    resultado = await use_case.executar(
        CriarUsuarioInput(
            nome=dados.nome, email=dados.email, senha=dados.senha, perfil=dados.perfil
        )
    )
    return UsuarioSchema(
        id=resultado.id,
        nome=resultado.nome,
        email=resultado.email,
        perfil=resultado.perfil,
        ativo=resultado.ativo,
    )
