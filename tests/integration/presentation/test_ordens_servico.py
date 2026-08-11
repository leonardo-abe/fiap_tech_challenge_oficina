from app.domain.usuario.value_objects import Perfil

from ._auth import auth_headers

_CLIENTE = {
    "nome": "Maria Silva",
    "documento": "11144477735",
    "email": "maria@x.com",
    "telefone": "11999998888",
}


async def _criar_cliente_e_veiculo(client) -> tuple[int, int]:
    cliente = (
        await client.post("/api/v1/clientes/", json=_CLIENTE, headers=auth_headers(Perfil.ADMIN))
    ).json()
    veiculo = (
        await client.post(
            "/api/v1/veiculos/",
            json={
                "cliente_id": cliente["id"],
                "placa": "ABC1234",
                "marca": "Fiat",
                "modelo": "Uno",
                "ano": 2015,
            },
            headers=auth_headers(Perfil.ADMIN),
        )
    ).json()
    return cliente["id"], veiculo["id"]


async def _criar_servico_e_peca(client) -> tuple[int, int]:
    servico = (
        await client.post(
            "/api/v1/servicos/",
            json={"nome": "Troca de óleo", "descricao": "Óleo", "preco": "80.00"},
            headers=auth_headers(Perfil.ADMIN),
        )
    ).json()
    peca = (
        await client.post(
            "/api/v1/pecas/",
            json={
                "nome": "Filtro",
                "descricao": "Filtro",
                "preco": "30.00",
                "quantidade_inicial": 10,
            },
            headers=auth_headers(Perfil.ADMIN),
        )
    ).json()
    return servico["id"], peca["id"]


async def _criar_ordem_com_itens(client) -> dict:
    cliente_id, veiculo_id = await _criar_cliente_e_veiculo(client)
    servico_id, peca_id = await _criar_servico_e_peca(client)

    resposta = await client.post(
        "/api/v1/ordens-servico/",
        json={
            "cliente_id": cliente_id,
            "veiculo_id": veiculo_id,
            "itens_servico": [{"servico_id": servico_id}],
            "itens_peca": [{"peca_id": peca_id, "quantidade": 2}],
        },
        headers=auth_headers(Perfil.ATENDENTE),
    )
    return resposta.json()


async def test_criar_ordem_servico_com_itens(client):
    ordem = await _criar_ordem_com_itens(client)

    assert ordem["status"] == "RECEBIDA"
    assert ordem["orcamento"]["total"] == "140.00"


async def test_criar_ordem_servico_sem_itens_retorna_422(client):
    cliente_id, veiculo_id = await _criar_cliente_e_veiculo(client)

    resposta = await client.post(
        "/api/v1/ordens-servico/",
        json={"cliente_id": cliente_id, "veiculo_id": veiculo_id},
        headers=auth_headers(Perfil.ATENDENTE),
    )

    assert resposta.status_code == 422


async def test_criar_ordem_servico_como_mecanico_retorna_403(client):
    cliente_id, veiculo_id = await _criar_cliente_e_veiculo(client)

    resposta = await client.post(
        "/api/v1/ordens-servico/",
        json={"cliente_id": cliente_id, "veiculo_id": veiculo_id},
        headers=auth_headers(Perfil.MECANICO),
    )

    assert resposta.status_code == 403


async def test_fluxo_completo_de_status(client):
    ordem = await _criar_ordem_com_itens(client)
    ordem_id = ordem["id"]

    diagnostico = await client.post(
        f"/api/v1/ordens-servico/{ordem_id}/diagnostico", headers=auth_headers(Perfil.MECANICO)
    )
    orcamento_gerado = await client.post(
        f"/api/v1/ordens-servico/{ordem_id}/orcamento/gerar", headers=auth_headers(Perfil.MECANICO)
    )
    aprovado = await client.post(
        f"/api/v1/ordens-servico/{ordem_id}/orcamento/aprovar",
        headers=auth_headers(Perfil.ATENDENTE),
    )
    finalizado = await client.post(
        f"/api/v1/ordens-servico/{ordem_id}/execucao/finalizar",
        headers=auth_headers(Perfil.MECANICO),
    )
    entregue = await client.post(
        f"/api/v1/ordens-servico/{ordem_id}/entrega", headers=auth_headers(Perfil.ATENDENTE)
    )

    assert diagnostico.status_code == 200
    assert diagnostico.json()["status"] == "EM_DIAGNOSTICO"
    assert orcamento_gerado.json()["status"] == "AGUARDANDO_APROVACAO"
    assert aprovado.json()["status"] == "EM_EXECUCAO"
    assert finalizado.json()["status"] == "FINALIZADA"
    assert entregue.json()["status"] == "ENTREGUE"


async def test_transicao_com_perfil_errado_retorna_403(client):
    ordem = await _criar_ordem_com_itens(client)

    resposta = await client.post(
        f"/api/v1/ordens-servico/{ordem['id']}/diagnostico", headers=auth_headers(Perfil.ATENDENTE)
    )

    assert resposta.status_code == 403


async def test_transicao_invalida_retorna_409(client):
    ordem = await _criar_ordem_com_itens(client)

    resposta = await client.post(
        f"/api/v1/ordens-servico/{ordem['id']}/entrega", headers=auth_headers(Perfil.ATENDENTE)
    )

    assert resposta.status_code == 409


async def test_cancelamento(client):
    ordem = await _criar_ordem_com_itens(client)

    resposta = await client.post(
        f"/api/v1/ordens-servico/{ordem['id']}/cancelamento", headers=auth_headers(Perfil.ATENDENTE)
    )

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "CANCELADA"


async def test_gerar_orcamento_notifica_cliente_por_log(client, caplog):
    ordem = await _criar_ordem_com_itens(client)
    ordem_id = ordem["id"]
    await client.post(
        f"/api/v1/ordens-servico/{ordem_id}/diagnostico", headers=auth_headers(Perfil.MECANICO)
    )

    with caplog.at_level("INFO"):
        resposta = await client.post(
            f"/api/v1/ordens-servico/{ordem_id}/orcamento/gerar",
            headers=auth_headers(Perfil.MECANICO),
        )

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "AGUARDANDO_APROVACAO"
    # NOTIFICACAO_BACKEND=log (padrão de dev/teste) - a "entrega" do orçamento ao
    # cliente vira uma linha de log em vez de um e-mail real (sem depender de rede).
    mensagens = [registro.getMessage() for registro in caplog.records]
    assert any(
        str(ordem_id) in mensagem and _CLIENTE["email"] in mensagem for mensagem in mensagens
    )


async def test_reprovacao(client):
    ordem = await _criar_ordem_com_itens(client)
    ordem_id = ordem["id"]
    await client.post(
        f"/api/v1/ordens-servico/{ordem_id}/diagnostico", headers=auth_headers(Perfil.MECANICO)
    )
    await client.post(
        f"/api/v1/ordens-servico/{ordem_id}/orcamento/gerar", headers=auth_headers(Perfil.MECANICO)
    )

    resposta = await client.post(
        f"/api/v1/ordens-servico/{ordem_id}/orcamento/reprovar",
        headers=auth_headers(Perfil.ATENDENTE),
    )

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "REPROVADA"


async def test_listar_e_buscar_administrativo(client):
    ordem = await _criar_ordem_com_itens(client)

    listagem = await client.get("/api/v1/ordens-servico/", headers=auth_headers(Perfil.MECANICO))
    busca = await client.get(
        f"/api/v1/ordens-servico/{ordem['id']}", headers=auth_headers(Perfil.ATENDENTE)
    )
    inexistente = await client.get("/api/v1/ordens-servico/999", headers=auth_headers(Perfil.ADMIN))

    assert listagem.status_code == 200
    assert len(listagem.json()) == 1
    assert busca.status_code == 200
    assert inexistente.status_code == 404


async def test_consulta_publica_de_status(client):
    ordem = await _criar_ordem_com_itens(client)

    correta = await client.get(
        f"/api/v1/ordens-servico/{ordem['id']}/status", params={"documento": "11144477735"}
    )
    errada = await client.get(
        f"/api/v1/ordens-servico/{ordem['id']}/status", params={"documento": "52998224725"}
    )
    inexistente = await client.get(
        "/api/v1/ordens-servico/999/status", params={"documento": "11144477735"}
    )
    # ID-004: documento mal formado não pode virar 422 - precisa ser 404 igual a um
    # ordem_id inexistente, senão um atacante distingue "OS existe" de "OS não existe"
    # sem precisar de nenhum documento válido.
    malformado = await client.get(
        f"/api/v1/ordens-servico/{ordem['id']}/status", params={"documento": "123"}
    )

    assert correta.status_code == 200
    assert correta.json()["status"] == "RECEBIDA"
    assert errada.status_code == 404
    assert inexistente.status_code == 404
    assert malformado.status_code == 404


async def test_relatorio_tempo_medio_execucao_apenas_admin(client):
    resposta_admin = await client.get(
        "/api/v1/ordens-servico/relatorios/tempo-medio-execucao", headers=auth_headers(Perfil.ADMIN)
    )
    resposta_atendente = await client.get(
        "/api/v1/ordens-servico/relatorios/tempo-medio-execucao",
        headers=auth_headers(Perfil.ATENDENTE),
    )

    assert resposta_admin.status_code == 200
    assert resposta_admin.json()["quantidade_ordens_finalizadas"] == 0
    assert resposta_atendente.status_code == 403


async def test_consulta_publica_de_status_com_muitas_tentativas_retorna_429(client):
    # ID-005: sem rate limiting, a rota pública de status podia ser varrida
    # sequencialmente por ordem_id sem limite. Limite configurado é 20/minuto por IP.
    respostas = [
        await client.get(
            "/api/v1/ordens-servico/999/status", params={"documento": "11144477735"}
        )
        for _ in range(21)
    ]

    assert [r.status_code for r in respostas[:20]] == [404] * 20
    assert respostas[20].status_code == 429
