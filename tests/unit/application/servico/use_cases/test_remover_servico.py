from decimal import Decimal

import pytest

from app.application.servico.dtos import CriarServicoInput
from app.application.servico.use_cases import CriarServicoUseCase, RemoverServicoUseCase
from app.domain.servico.exceptions import ServicoNaoEncontradoError
from tests.unit.application.fakes import FakeServicoRepository


async def test_remover_servico_sucesso():
    repositorio = FakeServicoRepository()
    criado = await CriarServicoUseCase(repositorio).executar(
        CriarServicoInput(nome="Troca de óleo", descricao="Óleo", preco=Decimal("120.00"))
    )

    await RemoverServicoUseCase(repositorio).executar(criado.id)

    assert await repositorio.buscar_por_id(criado.id) is None


async def test_remover_servico_inexistente_levanta_erro():
    use_case = RemoverServicoUseCase(FakeServicoRepository())

    with pytest.raises(ServicoNaoEncontradoError):
        await use_case.executar(999)
