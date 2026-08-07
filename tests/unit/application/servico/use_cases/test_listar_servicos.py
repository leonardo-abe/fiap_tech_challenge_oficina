from decimal import Decimal

from app.application.servico.dtos import CriarServicoInput
from app.application.servico.use_cases import CriarServicoUseCase, ListarServicosUseCase
from tests.unit.application.fakes import FakeServicoRepository


async def test_listar_servicos_vazio():
    resultado = await ListarServicosUseCase(FakeServicoRepository()).executar()

    assert resultado == []


async def test_listar_servicos_com_registros():
    repositorio = FakeServicoRepository()
    await CriarServicoUseCase(repositorio).executar(
        CriarServicoInput(nome="Troca de óleo", descricao="Óleo", preco=Decimal("120.00"))
    )
    await CriarServicoUseCase(repositorio).executar(
        CriarServicoInput(nome="Alinhamento", descricao="Alinhamento", preco=Decimal("80.00"))
    )

    resultado = await ListarServicosUseCase(repositorio).executar()

    assert len(resultado) == 2
