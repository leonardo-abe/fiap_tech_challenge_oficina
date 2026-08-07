from decimal import Decimal

from app.application.peca.dtos import CriarPecaInput
from app.application.peca.use_cases import CriarPecaUseCase, ListarPecasUseCase
from tests.unit.application.fakes import FakePecaRepository


async def test_listar_pecas_vazio():
    resultado = await ListarPecasUseCase(FakePecaRepository()).executar()

    assert resultado == []


async def test_listar_pecas_com_registros():
    repositorio = FakePecaRepository()
    await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Filtro", descricao="Filtro", preco=Decimal("39.90"), quantidade_inicial=10
        )
    )
    await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Vela", descricao="Vela de ignição", preco=Decimal("25.00"), quantidade_inicial=5
        )
    )

    resultado = await ListarPecasUseCase(repositorio).executar()

    assert len(resultado) == 2
