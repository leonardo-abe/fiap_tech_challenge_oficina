from decimal import Decimal

from app.domain.servico.entities import Servico
from app.domain.shared.value_objects import Money


def test_criar_servico():
    servico = Servico(
        nome="Troca de óleo",
        descricao="Troca de óleo e filtro",
        preco=Money(valor=Decimal("120.00")),
        id=1,
    )

    assert servico.nome == "Troca de óleo"
    assert servico.preco.valor == Decimal("120.00")
