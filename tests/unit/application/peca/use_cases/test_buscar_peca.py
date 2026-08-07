from decimal import Decimal

import pytest

from app.application.peca.dtos import CriarPecaInput
from app.application.peca.use_cases import BuscarPecaUseCase, CriarPecaUseCase
from app.domain.peca.exceptions import PecaNaoEncontradaError
from tests.unit.application.fakes import FakePecaRepository


async def test_buscar_peca_existente():
    repositorio = FakePecaRepository()
    criada = await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Filtro", descricao="Filtro", preco=Decimal("39.90"), quantidade_inicial=10
        )
    )

    resultado = await BuscarPecaUseCase(repositorio).executar(criada.id)

    assert resultado.nome == "Filtro"


async def test_buscar_peca_inexistente_levanta_erro():
    use_case = BuscarPecaUseCase(FakePecaRepository())

    with pytest.raises(PecaNaoEncontradaError):
        await use_case.executar(999)
