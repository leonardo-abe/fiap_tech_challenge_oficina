from decimal import Decimal

from app.domain.ordem_servico.entities import ItemServico
from app.domain.shared.value_objects import Money


def test_item_servico_guarda_snapshot_do_valor():
    item = ItemServico(servico_id=1, nome="Troca de óleo", valor=Money(valor=Decimal("80.00")))

    assert item.servico_id == 1
    assert item.valor.valor == Decimal("80.00")
