import pytest

from app.domain.cliente.exceptions import DocumentoInvalidoError
from app.domain.cliente.value_objects import Documento


@pytest.mark.parametrize("cpf", ["11144477735", "52998224725", "111.444.777-35"])
def test_documento_cpf_valido_normaliza_para_digitos(cpf):
    documento = Documento(valor=cpf)

    assert documento.valor == "".join(filter(str.isdigit, cpf))


def test_documento_cnpj_valido_normaliza_para_digitos():
    documento = Documento(valor="11.444.777/0001-61")

    assert documento.valor == "11444777000161"


@pytest.mark.parametrize(
    "valor_invalido",
    [
        "11111111111",  # CPF com dígitos repetidos
        "12345678900",  # CPF com dígito verificador incorreto
        "11111111111111",  # CNPJ com dígitos repetidos
        "11222333000199",  # CNPJ com dígito verificador incorreto
        "123",  # nem 11 nem 14 dígitos
        "",
    ],
)
def test_documento_invalido_levanta_erro(valor_invalido):
    with pytest.raises(DocumentoInvalidoError):
        Documento(valor=valor_invalido)
