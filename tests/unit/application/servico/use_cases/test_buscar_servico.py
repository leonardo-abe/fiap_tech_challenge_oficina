from decimal import Decimal

import pytest

from app.application.servico.dtos import CriarServicoInput
from app.application.servico.use_cases import BuscarServicoUseCase, CriarServicoUseCase
from app.domain.servico.exceptions import ServicoNaoEncontradoError
from tests.unit.application.fakes import FakeServicoRepository


async def test_buscar_servico_existente():
    repositorio = FakeServicoRepository()
    criado = await CriarServicoUseCase(repositorio).executar(
        CriarServicoInput(nome="Troca de óleo", descricao="Óleo", preco=Decimal("120.00"))
    )

    resultado = await BuscarServicoUseCase(repositorio).executar(criado.id)

    assert resultado.nome == "Troca de óleo"


async def test_buscar_servico_inexistente_levanta_erro():
    use_case = BuscarServicoUseCase(FakeServicoRepository())

    with pytest.raises(ServicoNaoEncontradoError):
        await use_case.executar(999)
