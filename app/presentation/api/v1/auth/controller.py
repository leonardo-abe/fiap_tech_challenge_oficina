from app.application.usuario.dtos import AutenticarUsuarioInput
from app.application.usuario.use_cases import AutenticarUsuarioUseCase
from app.presentation.api.v1.auth.schemas import LoginRequestSchema, TokenResponseSchema


class AuthController:
    def __init__(self, autenticar_use_case: AutenticarUsuarioUseCase) -> None:
        self._autenticar_use_case = autenticar_use_case

    async def login(self, dados: LoginRequestSchema) -> TokenResponseSchema:
        resultado = await self._autenticar_use_case.executar(
            AutenticarUsuarioInput(email=dados.email, senha=dados.senha)
        )
        return TokenResponseSchema(
            access_token=resultado.access_token, token_type=resultado.token_type
        )
