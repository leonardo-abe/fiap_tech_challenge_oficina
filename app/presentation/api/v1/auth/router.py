from fastapi import APIRouter, Depends, status

from app.application.usuario.dtos import AutenticarUsuarioInput
from app.application.usuario.use_cases import AutenticarUsuarioUseCase
from app.presentation.api.v1.auth.dependencies import get_autenticar_usuario_use_case
from app.presentation.api.v1.auth.schemas import LoginRequestSchema, TokenResponseSchema

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    dados: LoginRequestSchema,
    use_case: AutenticarUsuarioUseCase = Depends(get_autenticar_usuario_use_case),
) -> TokenResponseSchema:
    resultado = await use_case.executar(
        AutenticarUsuarioInput(email=dados.email, senha=dados.senha)
    )
    return TokenResponseSchema(access_token=resultado.access_token, token_type=resultado.token_type)
