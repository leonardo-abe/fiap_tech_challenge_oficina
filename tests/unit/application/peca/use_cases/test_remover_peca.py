from decimal import Decimal

import pytest

from app.application.peca.dtos import CriarPecaInput
from app.application.peca.use_cases import CriarPecaUseCase, RemoverPecaUseCase
from app.domain.peca.exceptions import PecaNaoEncontradaError
from tests.unit.application.fakes import FakePecaRepository


async def test_remover_peca_sucesso():
    repositorio = FakePecaRepository()
    criada = await CriarPecaUseCase(repositorio).executar(
        CriarPecaInput(
            nome="Filtro", descricao="Filtro", preco=Decimal("39.90"), quantidade_inicial=10
        )
    )

    await RemoverPecaUseCase(repositorio).executar(criada.id)

    assert await repositorio.buscar_por_id(criada.id) is None


async def test_remover_peca_inexistente_levanta_erro():
    use_case = RemoverPecaUseCase(FakePecaRepository())

    with pytest.raises(PecaNaoEncontradaError):
        await use_case.executar(999)
