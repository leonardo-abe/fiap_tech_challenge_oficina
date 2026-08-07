from app.domain.usuario.value_objects import Perfil

from ._auth import auth_headers


async def test_criar_usuario_como_admin(client):
    resposta = await client.post(
        "/api/v1/usuarios/",
        json={"nome": "João", "email": "joao@x.com", "senha": "segredo123", "perfil": "MECANICO"},
        headers=auth_headers(Perfil.ADMIN),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["email"] == "joao@x.com"
    assert corpo["perfil"] == "MECANICO"
    assert "senha" not in corpo


async def test_criar_usuario_sem_autenticacao_retorna_401(client):
    resposta = await client.post(
        "/api/v1/usuarios/",
        json={"nome": "João", "email": "joao@x.com", "senha": "segredo123", "perfil": "MECANICO"},
    )

    assert resposta.status_code == 401


async def test_criar_usuario_como_nao_admin_retorna_403(client):
    resposta = await client.post(
        "/api/v1/usuarios/",
        json={"nome": "João", "email": "joao@x.com", "senha": "segredo123", "perfil": "MECANICO"},
        headers=auth_headers(Perfil.ATENDENTE),
    )

    assert resposta.status_code == 403


async def test_criar_usuario_com_email_duplicado_retorna_409(client):
    dados = {"nome": "João", "email": "joao@x.com", "senha": "segredo123", "perfil": "MECANICO"}
    await client.post("/api/v1/usuarios/", json=dados, headers=auth_headers(Perfil.ADMIN))

    resposta = await client.post(
        "/api/v1/usuarios/", json=dados, headers=auth_headers(Perfil.ADMIN)
    )

    assert resposta.status_code == 409
