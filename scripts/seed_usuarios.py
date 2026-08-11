import asyncio

from app.application.usuario.dtos import CriarUsuarioInput
from app.application.usuario.use_cases import CriarUsuarioUseCase
from app.domain.usuario.exceptions import EmailJaCadastradoError
from app.domain.usuario.value_objects import Perfil
from app.infrastructure.db.session import SessionFactory
from app.infrastructure.persistence.usuario.repository import SQLAlchemyUsuarioRepository
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.shared.settings import settings

_USUARIOS_DE_TESTE = (
    ("Administrador", settings.seed_admin_email, settings.seed_admin_senha, Perfil.ADMIN),
    ("Atendente", settings.seed_atendente_email, settings.seed_atendente_senha, Perfil.ATENDENTE),
    ("Mecânico", settings.seed_mecanico_email, settings.seed_mecanico_senha, Perfil.MECANICO),
)


async def seed_usuarios() -> None:
    async with SessionFactory() as session:
        use_case = CriarUsuarioUseCase(
            usuario_repository=SQLAlchemyUsuarioRepository(session=session),
            password_hasher=BcryptPasswordHasher(),
        )
        for nome, email, senha, perfil in _USUARIOS_DE_TESTE:
            try:
                await use_case.executar(
                    CriarUsuarioInput(nome=nome, email=email, senha=senha, perfil=perfil)
                )
                # fora do ciclo de request do FastAPI: get_session não está aqui pra comitar,
                # então o script precisa comitar a própria Unit of Work explicitamente.
                await session.commit()
                print(f"Usuário criado: {email} ({perfil.value})")
            except EmailJaCadastradoError:
                await session.rollback()
                print(f"Usuário já existe: {email} ({perfil.value})")


if __name__ == "__main__":
    asyncio.run(seed_usuarios())
