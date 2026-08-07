from app.domain.usuario.entities import Usuario
from app.domain.usuario.value_objects import Perfil
from app.infrastructure.persistence.usuario.repository import SQLAlchemyUsuarioRepository
from app.infrastructure.security.password_hasher import BcryptPasswordHasher


async def _seed_usuario(session, email="admin@x.com", senha="segredo123", perfil=Perfil.ADMIN):
    hasher = BcryptPasswordHasher()
    await SQLAlchemyUsuarioRepository(session=session).criar(
        Usuario(nome="Admin", email=email, senha_hash=hasher.hash(senha), perfil=perfil)
    )
    await session.commit()


async def test_login_com_credenciais_validas_retorna_token(client, session):
    await _seed_usuario(session)

    resposta = await client.post(
        "/api/v1/auth/login", json={"email": "admin@x.com", "senha": "segredo123"}
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["token_type"] == "bearer"
    assert corpo["access_token"]


async def test_login_com_senha_incorreta_retorna_401(client, session):
    await _seed_usuario(session)

    resposta = await client.post(
        "/api/v1/auth/login", json={"email": "admin@x.com", "senha": "errada"}
    )

    assert resposta.status_code == 401


async def test_login_com_usuario_inexistente_retorna_401(client):
    resposta = await client.post(
        "/api/v1/auth/login", json={"email": "ninguem@x.com", "senha": "qualquer"}
    )

    assert resposta.status_code == 401


async def test_rota_protegida_com_token_malformado_retorna_401(client):
    resposta = await client.get(
        "/api/v1/clientes/", headers={"Authorization": "Bearer token-invalido"}
    )

    assert resposta.status_code == 401
