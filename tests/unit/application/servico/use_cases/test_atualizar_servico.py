from decimal import Decimal

import pytest

from app.application.servico.dtos import AtualizarServicoInput, CriarServicoInput
from app.application.servico.use_cases import AtualizarServicoUseCase, CriarServicoUseCase
from app.domain.servico.exceptions import ServicoNaoEncontradoError
from tests.unit.application.fakes import FakeServicoRepository


async def test_atualizar_servico_sucesso():
    repositorio = FakeServicoRepository()
    criado = await CriarServicoUseCase(repositorio).executar(
        CriarServicoInput(nome="Troca de óleo", descricao="Óleo", preco=Decimal("120.00"))
    )

    resultado = await AtualizarServicoUseCase(repositorio).executar(
        criado.id,
        AtualizarServicoInput(
            nome="Troca de óleo sintético", descricao="Óleo", preco=Decimal("150.00")
        ),
    )

    assert resultado.nome == "Troca de óleo sintético"
    assert resultado.preco == Decimal("150.00")


async def test_atualizar_servico_inexistente_levanta_erro():
    use_case = AtualizarServicoUseCase(FakeServicoRepository())

    with pytest.raises(ServicoNaoEncontradoError):
        await use_case.executar(
            999, AtualizarServicoInput(nome="Troca", descricao="Óleo", preco=Decimal("1"))
        )
