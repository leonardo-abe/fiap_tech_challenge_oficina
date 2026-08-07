from app.domain.usuario.value_objects import Perfil

from ._auth import auth_headers

_DADOS = {
    "nome": "Filtro de óleo",
    "descricao": "Filtro",
    "preco": "39.90",
    "quantidade_inicial": 10,
}


async def test_criar_peca_como_admin(client):
    resposta = await client.post("/api/v1/pecas/", json=_DADOS, headers=auth_headers(Perfil.ADMIN))

    assert resposta.status_code == 201
    assert resposta.json()["quantidade_disponivel"] == 10


async def test_criar_peca_como_mecanico_retorna_403(client):
    resposta = await client.post(
        "/api/v1/pecas/", json=_DADOS, headers=auth_headers(Perfil.MECANICO)
    )

    assert resposta.status_code == 403


async def test_listar_e_buscar_peca_com_qualquer_perfil(client):
    criada = (
        await client.post("/api/v1/pecas/", json=_DADOS, headers=auth_headers(Perfil.ADMIN))
    ).json()

    listagem = await client.get("/api/v1/pecas/", headers=auth_headers(Perfil.MECANICO))
    busca = await client.get(
        f"/api/v1/pecas/{criada['id']}", headers=auth_headers(Perfil.ATENDENTE)
    )

    assert listagem.status_code == 200
    assert busca.status_code == 200


async def test_repor_estoque(client):
    criada = (
        await client.post("/api/v1/pecas/", json=_DADOS, headers=auth_headers(Perfil.ADMIN))
    ).json()

    resposta = await client.patch(
        f"/api/v1/pecas/{criada['id']}/estoque",
        json={"quantidade": 5},
        headers=auth_headers(Perfil.ADMIN),
    )

    assert resposta.status_code == 200
    assert resposta.json()["quantidade_disponivel"] == 15


async def test_repor_estoque_com_quantidade_invalida_retorna_422(client):
    criada = (
        await client.post("/api/v1/pecas/", json=_DADOS, headers=auth_headers(Perfil.ADMIN))
    ).json()

    resposta = await client.patch(
        f"/api/v1/pecas/{criada['id']}/estoque",
        json={"quantidade": 0},
        headers=auth_headers(Perfil.ADMIN),
    )

    assert resposta.status_code == 422


async def test_atualizar_e_remover_peca(client):
    criada = (
        await client.post("/api/v1/pecas/", json=_DADOS, headers=auth_headers(Perfil.ADMIN))
    ).json()

    atualizada = await client.put(
        f"/api/v1/pecas/{criada['id']}",
        json={"nome": "Filtro premium", "descricao": "Filtro", "preco": "49.90"},
        headers=auth_headers(Perfil.ADMIN),
    )
    removida = await client.delete(
        f"/api/v1/pecas/{criada['id']}", headers=auth_headers(Perfil.ADMIN)
    )
    busca = await client.get(f"/api/v1/pecas/{criada['id']}", headers=auth_headers(Perfil.ADMIN))

    assert atualizada.status_code == 200
    assert atualizada.json()["nome"] == "Filtro premium"
    assert removida.status_code == 204
    assert busca.status_code == 404
