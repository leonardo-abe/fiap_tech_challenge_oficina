import secrets
from collections.abc import Callable
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.usuario.dtos import TokenPayload
from app.application.usuario.use_cases import AutenticarUsuarioUseCase, CriarUsuarioUseCase
from app.domain.usuario.value_objects import Perfil
from app.infrastructure.db.session import get_session
from app.infrastructure.persistence.usuario.repository import SQLAlchemyUsuarioRepository
from app.infrastructure.security.jwt_provider import JWTTokenProvider
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.presentation.api.v1.auth.controller import AuthController

_bearer_scheme = HTTPBearer(auto_error=False)


def get_usuario_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyUsuarioRepository:
    return SQLAlchemyUsuarioRepository(session=session)


def get_password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()


def get_token_provider() -> JWTTokenProvider:
    return JWTTokenProvider()


@lru_cache
def _get_hash_sem_correspondencia() -> str:
    # gerado uma vez por processo, a partir de um valor aleatório que ninguém conhece -
    # ver o comentário em AutenticarUsuarioUseCase.__init__ para o motivo de existir.
    return BcryptPasswordHasher().hash(secrets.token_urlsafe(32))


def get_autenticar_usuario_use_case(
    usuario_repository: SQLAlchemyUsuarioRepository = Depends(get_usuario_repository),
    password_hasher: BcryptPasswordHasher = Depends(get_password_hasher),
    token_provider: JWTTokenProvider = Depends(get_token_provider),
) -> AutenticarUsuarioUseCase:
    return AutenticarUsuarioUseCase(
        usuario_repository=usuario_repository,
        password_hasher=password_hasher,
        token_provider=token_provider,
        hash_sem_correspondencia=_get_hash_sem_correspondencia(),
    )


def get_auth_controller(
    autenticar_use_case: AutenticarUsuarioUseCase = Depends(get_autenticar_usuario_use_case),
) -> AuthController:
    return AuthController(autenticar_use_case=autenticar_use_case)


def get_criar_usuario_use_case(
    usuario_repository: SQLAlchemyUsuarioRepository = Depends(get_usuario_repository),
    password_hasher: BcryptPasswordHasher = Depends(get_password_hasher),
) -> CriarUsuarioUseCase:
    return CriarUsuarioUseCase(
        usuario_repository=usuario_repository, password_hasher=password_hasher
    )


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer_scheme)],
    token_provider: JWTTokenProvider = Depends(get_token_provider),
) -> TokenPayload:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_provider.decodificar_token(credentials.credentials)


def require_roles(*perfis_permitidos: Perfil) -> Callable[[TokenPayload], TokenPayload]:
    def _verificar(
        usuario_atual: Annotated[TokenPayload, Depends(get_current_user)],
    ) -> TokenPayload:
        if usuario_atual.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para executar esta ação.",
            )
        return usuario_atual

    return _verificar
