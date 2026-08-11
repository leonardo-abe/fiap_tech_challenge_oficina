from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.db.session import get_session
from app.infrastructure.notificacao.log_notificador_orcamento import LogNotificadorOrcamento
from app.infrastructure.security.rate_limiter import limiter
from app.main import app
from app.presentation.api.v1.ordens_servico.dependencies import get_notificador_orcamento

from ..conftest import truncate_all_tables


@pytest.fixture
async def client(engine) -> AsyncGenerator[AsyncClient, None]:
    # o ASGITransport não passa por uma conexão TCP real, então get_remote_address
    # devolve o mesmo "IP" para todos os testes - sem resetar, as chamadas de um teste
    # contam para o limite do próximo e a suíte começa a receber 429 de "vizinhos".
    limiter.reset()

    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def _get_test_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as db_session:
            try:
                yield db_session
                await db_session.commit()
            except Exception:
                await db_session.rollback()
                raise

    app.dependency_overrides[get_session] = _get_test_session
    # a suíte não pode depender de credenciais SMTP reais nem disparar e-mail de
    # verdade a cada execução - independente do NOTIFICACAO_BACKEND configurado no
    # .env de quem está rodando os testes localmente (ex.: para demo manual).
    app.dependency_overrides[get_notificador_orcamento] = LogNotificadorOrcamento

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client

    app.dependency_overrides.clear()
    await truncate_all_tables(engine)
