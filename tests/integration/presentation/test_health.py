from app.infrastructure.db.session import get_session
from app.main import app


async def test_health_com_banco_disponivel_retorna_ok(client):
    resposta = await client.get("/health")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["status"] == "ok"
    assert corpo["database"] == "ok"
    assert corpo["app_name"]
    assert corpo["environment"]
    assert corpo["verificado_em"]


async def test_health_com_banco_indisponivel_retorna_503(client):
    class _SessaoComFalha:
        async def execute(self, *args, **kwargs):
            raise ConnectionError("banco fora do ar")

    async def _sessao_com_falha():
        yield _SessaoComFalha()

    app.dependency_overrides[get_session] = _sessao_com_falha
    try:
        resposta = await client.get("/health")
    finally:
        app.dependency_overrides.pop(get_session, None)

    assert resposta.status_code == 503
    corpo = resposta.json()
    assert corpo["status"] == "degradado"
    assert corpo["database"] == "indisponivel"
