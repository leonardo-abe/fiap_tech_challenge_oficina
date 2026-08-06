from dataclasses import dataclass

from validate_docbr import CNPJ, CPF

from app.domain.cliente.exceptions.documento_invalido import DocumentoInvalidoError


@dataclass(frozen=True)
class Documento:
    valor: str

    def __post_init__(self) -> None:
        numeros = "".join(filter(str.isdigit, self.valor))
        if len(numeros) == 11:
            valido = CPF().validate(numeros)
        elif len(numeros) == 14:
            valido = CNPJ().validate(numeros)
        else:
            valido = False

        if not valido:
            raise DocumentoInvalidoError(self.valor)

        # normaliza para dígitos puros - dataclass é frozen, então o ajuste
        # pós-validação exige contornar a imutabilidade desta forma.
        object.__setattr__(self, "valor", numeros)
