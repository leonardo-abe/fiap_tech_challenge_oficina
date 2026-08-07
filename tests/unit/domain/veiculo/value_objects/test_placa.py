import pytest

from app.domain.veiculo.exceptions import PlacaInvalidaError
from app.domain.veiculo.value_objects import Placa


@pytest.mark.parametrize(
    "valor,normalizado",
    [
        ("ABC1234", "ABC1234"),
        ("abc-1234", "ABC1234"),
        ("ABC 1234", "ABC1234"),
        ("ABC1D23", "ABC1D23"),
        ("abc1d23", "ABC1D23"),
    ],
)
def test_placa_valida_normaliza(valor, normalizado):
    placa = Placa(valor=valor)

    assert placa.valor == normalizado


@pytest.mark.parametrize(
    "valor_invalido",
    [
        "AB1234",  # só 2 letras
        "ABCD1234",  # 4 letras
        "ABC12345",  # 5 dígitos
        "ABC123",  # 3 dígitos
        "123ABC4",  # ordem errada
        "",
    ],
)
def test_placa_invalida_levanta_erro(valor_invalido):
    with pytest.raises(PlacaInvalidaError):
        Placa(valor=valor_invalido)
