from decimal import Decimal

import pytest

from app.application.peca.dtos import CriarPecaInput
from app.application.peca.use_cases import CriarPecaUseCase
from app.domain.peca.exceptions import QuantidadeInvalidaError
from tests.unit.application.fakes import FakePecaRepository


async def test_criar_peca_sucesso():
    use_case = CriarPecaUseCase(FakePecaRepository())

    resultado = await use_case.executar(
        CriarPecaInput(
            nome="Filtro de óleo", descricao="Filtro", preco=Decimal("39.90"), quantidade_inicial=10
        )
    )

    assert resultado.id == 1
    assert resultado.quantidade_disponivel == 10


async def test_criar_peca_com_quantidade_negativa_levanta_erro():
    use_case = CriarPecaUseCase(FakePecaRepository())

    with pytest.raises(QuantidadeInvalidaError):
        await use_case.executar(
            CriarPecaInput(
                nome="Filtro", descricao="Filtro", preco=Decimal("39.90"), quantidade_inicial=-1
            )
        )
