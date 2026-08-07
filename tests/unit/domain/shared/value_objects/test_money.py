from decimal import Decimal

import pytest

from app.domain.shared.exceptions import ValorMonetarioInvalidoError
from app.domain.shared.value_objects import Money


def test_money_quantiza_para_duas_casas_decimais():
    money = Money(valor=Decimal("10.005"))

    assert money.valor == Decimal("10.01")


def test_money_com_valor_negativo_levanta_erro():
    with pytest.raises(ValorMonetarioInvalidoError):
        Money(valor=Decimal("-1"))


def test_money_com_valor_nao_numerico_levanta_erro():
    with pytest.raises(ValorMonetarioInvalidoError):
        Money(valor="abc")


def test_money_somar():
    resultado = Money(valor=Decimal("10.00")).somar(Money(valor=Decimal("5.50")))

    assert resultado.valor == Decimal("15.50")


def test_money_multiplicar():
    resultado = Money(valor=Decimal("10.00")).multiplicar(3)

    assert resultado.valor == Decimal("30.00")
