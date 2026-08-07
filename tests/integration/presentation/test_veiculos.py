from app.domain.usuario.value_objects import Perfil

from ._auth import auth_headers

_CLIENTE = {
    "nome": "Maria Silva",
    "documento": "11144477735",
    "email": "maria@x.com",
    "telefone": "11999998888",
}


async def _criar_cliente(client) -> int:
    resposta = await client.post(
        "/api/v1/clientes/", json=_CLIENTE, headers=auth_headers(Perfil.ADMIN)
    )
    return resposta.json()["id"]


def _dados_veiculo(cliente_id: int, placa="ABC1234") -> dict:
    return {"cliente_id": cliente_id, "placa": placa, "marca": "Fiat", "modelo": "Uno", "ano": 2015}


async def test_criar_veiculo_como_atendente(client):
    cliente_id = await _criar_cliente(client)

    resposta = await client.post(
        "/api/v1/veiculos/", json=_dados_veiculo(cliente_id), headers=auth_headers(Perfil.ATENDENTE)
    )

    assert resposta.status_code == 201
    assert resposta.json()["placa"] == "ABC1234"


async def test_criar_veiculo_como_mecanico_retorna_403(client):
    cliente_id = await _criar_cliente(client)

    resposta = await client.post(
        "/api/v1/veiculos/", json=_dados_veiculo(cliente_id), headers=auth_headers(Perfil.MECANICO)
    )

    assert resposta.status_code == 403


async def test_criar_veiculo_com_cliente_inexistente_retorna_404(client):
    resposta = await client.post(
        "/api/v1/veiculos/", json=_dados_veiculo(999), headers=auth_headers(Perfil.ADMIN)
    )

    assert resposta.status_code == 404


async def test_criar_veiculo_com_placa_invalida_retorna_422(client):
    cliente_id = await _criar_cliente(client)

    resposta = await client.post(
        "/api/v1/veiculos/",
        json=_dados_veiculo(cliente_id, placa="1234567"),
        headers=auth_headers(Perfil.ADMIN),
    )

    assert resposta.status_code == 422


async def test_listar_veiculos_filtra_por_cliente(client):
    cliente_1 = await _criar_cliente(client)
    outro_cliente = (
        await client.post(
            "/api/v1/clientes/",
            json={**_CLIENTE, "documento": "52998224725", "email": "j@x.com"},
            headers=auth_headers(Perfil.ADMIN),
        )
    ).json()["id"]
    await client.post(
        "/api/v1/veiculos/", json=_dados_veiculo(cliente_1), headers=auth_headers(Perfil.ADMIN)
    )
    await client.post(
        "/api/v1/veiculos/",
        json=_dados_veiculo(outro_cliente, placa="DEF5678"),
        headers=auth_headers(Perfil.ADMIN),
    )

    resposta = await client.get(
        "/api/v1/veiculos/", params={"cliente_id": cliente_1}, headers=auth_headers(Perfil.ADMIN)
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["placa"] == "ABC1234"


async def test_buscar_veiculo_inexistente_retorna_404(client):
    resposta = await client.get("/api/v1/veiculos/999", headers=auth_headers(Perfil.ADMIN))

    assert resposta.status_code == 404


async def test_atualizar_e_remover_veiculo(client):
    cliente_id = await _criar_cliente(client)
    criado = (
        await client.post(
            "/api/v1/veiculos/", json=_dados_veiculo(cliente_id), headers=auth_headers(Perfil.ADMIN)
        )
    ).json()

    atualizado = await client.put(
        f"/api/v1/veiculos/{criado['id']}",
        json=_dados_veiculo(cliente_id, placa="DEF5678"),
        headers=auth_headers(Perfil.ADMIN),
    )
    removido = await client.delete(
        f"/api/v1/veiculos/{criado['id']}", headers=auth_headers(Perfil.ADMIN)
    )
    busca = await client.get(f"/api/v1/veiculos/{criado['id']}", headers=auth_headers(Perfil.ADMIN))

    assert atualizado.status_code == 200
    assert atualizado.json()["placa"] == "DEF5678"
    assert removido.status_code == 204
    assert busca.status_code == 404
