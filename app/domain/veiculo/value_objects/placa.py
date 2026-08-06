import re
from dataclasses import dataclass

from app.domain.veiculo.exceptions.placa_invalida import PlacaInvalidaError

_PADRAO_ANTIGO = re.compile(r"^[A-Z]{3}[0-9]{4}$")
_PADRAO_MERCOSUL = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")


@dataclass(frozen=True)
class Placa:
    valor: str

    def __post_init__(self) -> None:
        normalizada = "".join(filter(str.isalnum, self.valor)).upper()
        valida = bool(_PADRAO_ANTIGO.match(normalizada) or _PADRAO_MERCOSUL.match(normalizada))
        if not valida:
            raise PlacaInvalidaError(self.valor)

        # normaliza para o formato canônico (sem hífen/espaço, maiúsculo) - dataclass é
        # frozen, então o ajuste pós-validação exige contornar a imutabilidade desta forma.
        object.__setattr__(self, "valor", normalizada)
