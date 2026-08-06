import asyncio

from app.application.usuario.dtos import CriarUsuarioInput
from app.application.usuario.use_cases import CriarUsuarioUseCase
from app.domain.usuario.exceptions import EmailJaCadastradoError
from app.domain.usuario.value_objects import Perfil
from app.infrastructure.db.session import SessionFactory
from app.infrastructure.persistence.usuario.repository import SQLAlchemyUsuarioRepository
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.shared.settings import settings


async def seed_admin() -> None:
    async with SessionFactory() as session:
        use_case = CriarUsuarioUseCase(
            usuario_repository=SQLAlchemyUsuarioRepository(session=session),
            password_hasher=BcryptPasswordHasher(),
        )
        try:
            await use_case.executar(
                CriarUsuarioInput(
                    nome="Administrador",
                    email=settings.seed_admin_email,
                    senha=settings.seed_admin_senha,
                    perfil=Perfil.ADMIN,
                )
            )
            # fora do ciclo de request do FastAPI: get_session não está aqui pra comitar,
            # então o script precisa comitar a própria Unit of Work explicitamente.
            await session.commit()
            print(f"Admin criado: {settings.seed_admin_email}")
        except EmailJaCadastradoError:
            print(f"Admin já existe: {settings.seed_admin_email}")


if __name__ == "__main__":
    asyncio.run(seed_admin())
