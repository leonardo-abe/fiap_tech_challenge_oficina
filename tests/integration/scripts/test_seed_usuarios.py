from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

import scripts.seed_usuarios as seed_usuarios_module
from app.infrastructure.persistence.usuario.models import UsuarioModel
from app.infrastructure.persistence.usuario.repository import SQLAlchemyUsuarioRepository
from app.shared.settings import settings

from ..conftest import truncate_all_tables

_EMAILS_ESPERADOS = {
    settings.seed_admin_email: "ADMIN",
    settings.seed_atendente_email: "ATENDENTE",
    settings.seed_mecanico_email: "MECANICO",
}


async def _contar_por_email(session_factory, email: str) -> int:
    async with session_factory() as session:
        resultado = await session.execute(
            select(UsuarioModel).where(UsuarioModel.email == email)
        )
        return len(resultado.scalars().all())


async def test_seed_usuarios_cria_um_por_perfil_e_e_idempotente(engine, monkeypatch):
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(seed_usuarios_module, "SessionFactory", session_factory)

    await seed_usuarios_module.seed_usuarios()

    async with session_factory() as session:
        repositorio = SQLAlchemyUsuarioRepository(session=session)
        for email, perfil_esperado in _EMAILS_ESPERADOS.items():
            usuario = await repositorio.buscar_por_email(email)
            assert usuario is not None
            assert usuario.perfil.value == perfil_esperado
            assert usuario.ativo is True

    for email in _EMAILS_ESPERADOS:
        assert await _contar_por_email(session_factory, email) == 1

    # idempotente: rodar de novo não duplica nem levanta erro (EmailJaCadastradoError
    # é capturado e tratado dentro do próprio script, um usuário por vez).
    await seed_usuarios_module.seed_usuarios()

    for email in _EMAILS_ESPERADOS:
        assert await _contar_por_email(session_factory, email) == 1

    await truncate_all_tables(engine)
