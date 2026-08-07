from decimal import Decimal

from app.domain.ordem_servico.value_objects import Orcamento
from app.domain.shared.value_objects import Money


def test_orcamento_total_soma_servicos_e_pecas():
    orcamento = Orcamento(
        total_servicos=Money(valor=Decimal("100.00")),
        total_pecas=Money(valor=Decimal("50.00")),
    )

    assert orcamento.total.valor == Decimal("150.00")
