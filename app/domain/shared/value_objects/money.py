from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from app.domain.shared.exceptions.valor_monetario_invalido import ValorMonetarioInvalidoError

_CENTAVOS = Decimal("0.01")


@dataclass(frozen=True)
class Money:
    valor: Decimal

    def __post_init__(self) -> None:
        try:
            quantizado = Decimal(self.valor).quantize(_CENTAVOS, rounding=ROUND_HALF_UP)
        except InvalidOperation as erro:
            raise ValorMonetarioInvalidoError(str(self.valor)) from erro

        if quantizado < 0:
            raise ValorMonetarioInvalidoError(str(self.valor))

        # dataclass é frozen: normaliza para 2 casas decimais contornando a imutabilidade.
        object.__setattr__(self, "valor", quantizado)

    def somar(self, outro: "Money") -> "Money":
        return Money(valor=self.valor + outro.valor)

    def multiplicar(self, quantidade: int) -> "Money":
        return Money(valor=self.valor * quantidade)
