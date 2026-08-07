from app.domain.cliente.entities import Cliente
from app.domain.cliente.value_objects import Documento


def test_criar_cliente():
    cliente = Cliente(
        nome="Maria Silva",
        documento=Documento(valor="11144477735"),
        email="maria@example.com",
        telefone="11999998888",
        id=1,
    )

    assert cliente.nome == "Maria Silva"
    assert cliente.documento.valor == "11144477735"
