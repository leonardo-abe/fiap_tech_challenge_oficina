from app.domain.veiculo.entities import Veiculo
from app.domain.veiculo.value_objects import Placa


def test_criar_veiculo():
    veiculo = Veiculo(
        cliente_id=1,
        placa=Placa(valor="ABC1234"),
        marca="Fiat",
        modelo="Uno",
        ano=2015,
        id=1,
    )

    assert veiculo.cliente_id == 1
    assert veiculo.placa.valor == "ABC1234"
