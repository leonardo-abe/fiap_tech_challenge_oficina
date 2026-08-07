from decimal import Decimal

import pytest

from app.application.servico.dtos import CriarServicoInput
from app.application.servico.use_cases import CriarServicoUseCase
from app.domain.shared.exceptions import ValorMonetarioInvalidoError
from tests.unit.application.fakes import FakeServicoRepository


async def test_criar_servico_sucesso():
    use_case = CriarServicoUseCase(FakeServicoRepository())

    resultado = await use_case.executar(
        CriarServicoInput(nome="Troca de óleo", descricao="Óleo e filtro", preco=Decimal("120.00"))
    )

    assert resultado.id == 1
    assert resultado.preco == Decimal("120.00")


async def test_criar_servico_com_preco_negativo_levanta_erro():
    use_case = CriarServicoUseCase(FakeServicoRepository())

    with pytest.raises(ValorMonetarioInvalidoError):
        await use_case.executar(
            CriarServicoInput(nome="Troca de óleo", descricao="Óleo", preco=Decimal("-1"))
        )
