from app.domain.usuario.entities import Usuario
from app.domain.usuario.value_objects import Perfil
from app.infrastructure.persistence.usuario.repository import SQLAlchemyUsuarioRepository


def _usuario(email="joao@x.com") -> Usuario:
    return Usuario(nome="João", email=email, senha_hash="hash-opaco", perfil=Perfil.MECANICO)


async def test_criar_e_buscar_por_id(session):
    repositorio = SQLAlchemyUsuarioRepository(session=session)

    criado = await repositorio.criar(_usuario())

    assert criado.id is not None
    encontrado = await repositorio.buscar_por_id(criado.id)
    assert encontrado.email == "joao@x.com"
    assert encontrado.perfil == Perfil.MECANICO
    assert encontrado.ativo is True


async def test_buscar_por_id_inexistente_retorna_none(session):
    repositorio = SQLAlchemyUsuarioRepository(session=session)

    assert await repositorio.buscar_por_id(999) is None


async def test_buscar_por_email(session):
    repositorio = SQLAlchemyUsuarioRepository(session=session)
    await repositorio.criar(_usuario(email="joao@x.com"))

    encontrado = await repositorio.buscar_por_email("joao@x.com")
    inexistente = await repositorio.buscar_por_email("ninguem@x.com")

    assert encontrado.nome == "João"
    assert inexistente is None


async def test_existe_com_email(session):
    repositorio = SQLAlchemyUsuarioRepository(session=session)
    await repositorio.criar(_usuario(email="joao@x.com"))

    assert await repositorio.existe_com_email("joao@x.com") is True
    assert await repositorio.existe_com_email("ninguem@x.com") is False
