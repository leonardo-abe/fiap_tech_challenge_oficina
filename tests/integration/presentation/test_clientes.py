from app.domain.usuario.value_objects import Perfil

from ._auth import auth_headers

_DADOS = {
    "nome": "Maria Silva",
    "documento": "11144477735",
    "email": "maria@x.com",
    "telefone": "11999998888",
}


async def test_criar_cliente_como_atendente(client):
    resposta = await client.post(
        "/api/v1/clientes/", json=_DADOS, headers=auth_headers(Perfil.ATENDENTE)
    )

    assert resposta.status_code == 201
    assert resposta.json()["documento"] == "11144477735"


async def test_criar_cliente_sem_autenticacao_retorna_401(client):
    resposta = await client.post("/api/v1/clientes/", json=_DADOS)

    assert resposta.status_code == 401


async def test_criar_cliente_como_mecanico_retorna_403(client):
    resposta = await client.post(
        "/api/v1/clientes/", json=_DADOS, headers=auth_headers(Perfil.MECANICO)
    )

    assert resposta.status_code == 403


async def test_criar_cliente_com_documento_invalido_retorna_422(client):
    dados = {**_DADOS, "documento": "12345678901"}

    resposta = await client.post(
        "/api/v1/clientes/", json=dados, headers=auth_headers(Perfil.ADMIN)
    )

    assert resposta.status_code == 422


async def test_criar_cliente_com_documento_duplicado_retorna_409(client):
    await client.post("/api/v1/clientes/", json=_DADOS, headers=auth_headers(Perfil.ADMIN))

    resposta = await client.post(
        "/api/v1/clientes/", json=_DADOS, headers=auth_headers(Perfil.ADMIN)
    )

    assert resposta.status_code == 409


async def test_listar_e_buscar_cliente(client):
    criado = (
        await client.post("/api/v1/clientes/", json=_DADOS, headers=auth_headers(Perfil.ADMIN))
    ).json()

    listagem = await client.get("/api/v1/clientes/", headers=auth_headers(Perfil.ADMIN))
    busca = await client.get(f"/api/v1/clientes/{criado['id']}", headers=auth_headers(Perfil.ADMIN))

    assert listagem.status_code == 200
    assert len(listagem.json()) == 1
    assert busca.status_code == 200
    assert busca.json()["nome"] == "Maria Silva"


async def test_buscar_cliente_inexistente_retorna_404(client):
    resposta = await client.get("/api/v1/clientes/999", headers=auth_headers(Perfil.ADMIN))

    assert resposta.status_code == 404


async def test_atualizar_cliente(client):
    criado = (
        await client.post("/api/v1/clientes/", json=_DADOS, headers=auth_headers(Perfil.ADMIN))
    ).json()

    resposta = await client.put(
        f"/api/v1/clientes/{criado['id']}",
        json={**_DADOS, "nome": "Maria Souza"},
        headers=auth_headers(Perfil.ADMIN),
    )

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Maria Souza"


async def test_remover_cliente(client):
    criado = (
        await client.post("/api/v1/clientes/", json=_DADOS, headers=auth_headers(Perfil.ADMIN))
    ).json()

    resposta = await client.delete(
        f"/api/v1/clientes/{criado['id']}", headers=auth_headers(Perfil.ADMIN)
    )
    busca = await client.get(f"/api/v1/clientes/{criado['id']}", headers=auth_headers(Perfil.ADMIN))

    assert resposta.status_code == 204
    assert busca.status_code == 404
