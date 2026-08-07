from decimal import Decimal

import pytest

from app.domain.peca.entities import Peca
from app.domain.peca.exceptions import EstoqueInsuficienteError, QuantidadeInvalidaError
from app.domain.shared.value_objects import Money


def _criar_peca(quantidade_disponivel: int = 10) -> Peca:
    return Peca(
        nome="Filtro de óleo",
        descricao="Filtro de óleo compatível com motores 1.0/1.6",
        preco=Money(valor=Decimal("39.90")),
        quantidade_disponivel=quantidade_disponivel,
        id=1,
    )


def test_criar_peca_com_quantidade_valida():
    peca = _criar_peca(quantidade_disponivel=5)

    assert peca.quantidade_disponivel == 5


def test_criar_peca_com_quantidade_negativa_levanta_erro():
    with pytest.raises(QuantidadeInvalidaError):
        _criar_peca(quantidade_disponivel=-1)


def test_baixar_estoque_decrementa_quantidade():
    peca = _criar_peca(quantidade_disponivel=10)

    peca.baixar_estoque(4)

    assert peca.quantidade_disponivel == 6


def test_baixar_estoque_com_quantidade_zero_ou_negativa_levanta_erro():
    peca = _criar_peca(quantidade_disponivel=10)

    with pytest.raises(QuantidadeInvalidaError):
        peca.baixar_estoque(0)

    with pytest.raises(QuantidadeInvalidaError):
        peca.baixar_estoque(-3)


def test_baixar_estoque_maior_que_disponivel_levanta_erro():
    peca = _criar_peca(quantidade_disponivel=2)

    with pytest.raises(EstoqueInsuficienteError):
        peca.baixar_estoque(3)

    assert peca.quantidade_disponivel == 2


def test_repor_estoque_incrementa_quantidade():
    peca = _criar_peca(quantidade_disponivel=10)

    peca.repor_estoque(5)

    assert peca.quantidade_disponivel == 15


def test_repor_estoque_com_quantidade_zero_ou_negativa_levanta_erro():
    peca = _criar_peca(quantidade_disponivel=10)

    with pytest.raises(QuantidadeInvalidaError):
        peca.repor_estoque(0)

    with pytest.raises(QuantidadeInvalidaError):
        peca.repor_estoque(-1)
