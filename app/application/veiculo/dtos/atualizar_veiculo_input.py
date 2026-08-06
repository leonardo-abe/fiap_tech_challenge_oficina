from dataclasses import dataclass


@dataclass(frozen=True)
class AtualizarVeiculoInput:
    cliente_id: int
    placa: str
    marca: str
    modelo: str
    ano: int
