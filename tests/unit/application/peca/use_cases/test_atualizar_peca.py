from decimal import Decimal

import pytest

from app.application.peca.dtos import AtualizarPecaInput, CriarPecaInput
from app.application.peca.use_cases import AtualizarPecaUseCase, CriarPecaUseCase
from app.domain.peca.exceptions import PecaNaoEncontradaError
from tests.unit.application.fakes import FakePecaRepository


async def test_atualizar_peca_sucesso():
    repositorio = FakePecaRepository()
    criada = await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Filtro", descricao="Filtro", preco=Decimal("39.90"), quantidade_inicial=10
        )
    )

    resultado = await AtualizarPecaUseCase(repositorio).executar(
        criada.id,
        AtualizarPecaInput(nome="Filtro premium", descricao="Filtro", preco=Decimal("49.90")),
    )

    assert resultado.nome == "Filtro premium"
    assert resultado.preco == Decimal("49.90")
    assert resultado.quantidade_disponivel == 10


async def test_atualizar_peca_inexistente_levanta_erro():
    use_case = AtualizarPecaUseCase(FakePecaRepository())

    with pytest.raises(PecaNaoEncontradaError):
        await use_case.executar(
            999, AtualizarPecaInput(nome="Filtro", descricao="Filtro", preco=Decimal("1"))
        )
