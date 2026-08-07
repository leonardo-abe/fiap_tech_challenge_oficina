from decimal import Decimal

import pytest

from app.application.peca.dtos import CriarPecaInput, ReporEstoqueInput
from app.application.peca.use_cases import CriarPecaUseCase, ReporEstoqueUseCase
from app.domain.peca.exceptions import PecaNaoEncontradaError, QuantidadeInvalidaError
from tests.unit.application.fakes import FakePecaRepository


async def test_repor_estoque_sucesso():
    repositorio = FakePecaRepository()
    criada = await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Filtro", descricao="Filtro", preco=Decimal("39.90"), quantidade_inicial=10
        )
    )

    resultado = await ReporEstoqueUseCase(repositorio).executar(
        criada.id, ReporEstoqueInput(quantidade=5)
    )

    assert resultado.quantidade_disponivel == 15


async def test_repor_estoque_peca_inexistente_levanta_erro():
    use_case = ReporEstoqueUseCase(FakePecaRepository())

    with pytest.raises(PecaNaoEncontradaError):
        await use_case.executar(999, ReporEstoqueInput(quantidade=5))


async def test_repor_estoque_com_quantidade_invalida_levanta_erro():
    repositorio = FakePecaRepository()
    criada = await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Filtro", descricao="Filtro", preco=Decimal("39.90"), quantidade_inicial=10
        )
    )

    with pytest.raises(QuantidadeInvalidaError):
        await ReporEstoqueUseCase(repositorio).executar(criada.id, ReporEstoqueInput(quantidade=0))
