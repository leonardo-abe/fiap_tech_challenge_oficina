from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

import scripts.seed_admin as seed_admin_module
from app.infrastructure.persistence.usuario.models import UsuarioModel
from app.infrastructure.persistence.usuario.repository import SQLAlchemyUsuarioRepository
from app.shared.settings import settings

from ..conftest import truncate_all_tables


async def _contar_admins(session_factory) -> int:
    async with session_factory() as session:
        resultado = await session.execute(
            select(UsuarioModel).where(UsuarioModel.email == settings.seed_admin_email)
        )
        return len(resultado.scalars().all())


async def test_seed_admin_cria_e_e_idempotente(engine, monkeypatch):
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(seed_admin_module, "SessionFactory", session_factory)

    await seed_admin_module.seed_admin()

    async with session_factory() as session:
        usuario = await SQLAlchemyUsuarioRepository(session=session).buscar_por_email(
            settings.seed_admin_email
        )
        assert usuario is not None
        assert usuario.perfil.value == "ADMIN"
        assert usuario.ativo is True
    assert await _contar_admins(session_factory) == 1

    # idempotente: rodar de novo não duplica nem levanta erro (EmailJaCadastradoError
    # é capturado e tratado dentro do próprio script).
    await seed_admin_module.seed_admin()

    assert await _contar_admins(session_factory) == 1

    await truncate_all_tables(engine)
