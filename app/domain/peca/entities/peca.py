from dataclasses import dataclass

from app.domain.peca.exceptions.estoque_insuficiente import EstoqueInsuficienteError
from app.domain.peca.exceptions.quantidade_invalida import QuantidadeInvalidaError
from app.domain.shared.value_objects import Money


@dataclass
class Peca:
    nome: str
    descricao: str
    preco: Money
    quantidade_disponivel: int
    id: int | None = None

    def __post_init__(self) -> None:
        if self.quantidade_disponivel < 0:
            raise QuantidadeInvalidaError(self.quantidade_disponivel)

    def baixar_estoque(self, quantidade: int) -> None:
        if quantidade <= 0:
            raise QuantidadeInvalidaError(quantidade)
        if quantidade > self.quantidade_disponivel:
            raise EstoqueInsuficienteError(self.id, self.quantidade_disponivel, quantidade)

        self.quantidade_disponivel -= quantidade

    def repor_estoque(self, quantidade: int) -> None:
        if quantidade <= 0:
            raise QuantidadeInvalidaError(quantidade)

        self.quantidade_disponivel += quantidade
