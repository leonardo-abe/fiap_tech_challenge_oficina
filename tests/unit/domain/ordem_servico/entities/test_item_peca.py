from decimal import Decimal

import pytest

from app.domain.ordem_servico.entities import ItemPeca
from app.domain.ordem_servico.exceptions import QuantidadeItemInvalidaError
from app.domain.shared.value_objects import Money


def test_item_peca_calcula_valor_total():
    item = ItemPeca(
        peca_id=1, nome="Filtro", quantidade=3, valor_unitario=Money(valor=Decimal("25.00"))
    )

    assert item.valor_total.valor == Decimal("75.00")


def test_item_peca_com_quantidade_zero_ou_negativa_levanta_erro():
    with pytest.raises(QuantidadeItemInvalidaError):
        ItemPeca(peca_id=1, nome="Filtro", quantidade=0, valor_unitario=Money(valor=Decimal("1")))

    with pytest.raises(QuantidadeItemInvalidaError):
        ItemPeca(
            peca_id=1, nome="Filtro", quantidade=-2, valor_unitario=Money(valor=Decimal("1"))
        )
