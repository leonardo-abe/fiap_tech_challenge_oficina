from app.domain.usuario.value_objects import Perfil

from ._auth import auth_headers

_DADOS = {"nome": "Troca de óleo", "descricao": "Óleo e filtro", "preco": "120.00"}


async def test_criar_servico_como_admin(client):
    resposta = await client.post(
        "/api/v1/servicos/", json=_DADOS, headers=auth_headers(Perfil.ADMIN)
    )

    assert resposta.status_code == 201
    assert resposta.json()["preco"] == "120.00"


async def test_criar_servico_como_atendente_retorna_403(client):
    resposta = await client.post(
        "/api/v1/servicos/", json=_DADOS, headers=auth_headers(Perfil.ATENDENTE)
    )

    assert resposta.status_code == 403


async def test_listar_e_buscar_servico_com_qualquer_perfil(client):
    criado = (
        await client.post("/api/v1/servicos/", json=_DADOS, headers=auth_headers(Perfil.ADMIN))
    ).json()

    listagem = await client.get("/api/v1/servicos/", headers=auth_headers(Perfil.MECANICO))
    busca = await client.get(
        f"/api/v1/servicos/{criado['id']}", headers=auth_headers(Perfil.ATENDENTE)
    )

    assert listagem.status_code == 200
    assert len(listagem.json()) == 1
    assert busca.status_code == 200


async def test_buscar_servico_inexistente_retorna_404(client):
    resposta = await client.get("/api/v1/servicos/999", headers=auth_headers(Perfil.MECANICO))

    assert resposta.status_code == 404


async def test_atualizar_e_remover_servico(client):
    criado = (
        await client.post("/api/v1/servicos/", json=_DADOS, headers=auth_headers(Perfil.ADMIN))
    ).json()

    atualizado = await client.put(
        f"/api/v1/servicos/{criado['id']}",
        json={**_DADOS, "preco": "150.00"},
        headers=auth_headers(Perfil.ADMIN),
    )
    removido = await client.delete(
        f"/api/v1/servicos/{criado['id']}", headers=auth_headers(Perfil.ADMIN)
    )
    busca = await client.get(
        f"/api/v1/servicos/{criado['id']}", headers=auth_headers(Perfil.ADMIN)
    )

    assert atualizado.status_code == 200
    assert atualizado.json()["preco"] == "150.00"
    assert removido.status_code == 204
    assert busca.status_code == 404
