from dataclasses import dataclass


@dataclass(frozen=True)
class VeiculoOutput:
    id: int
    cliente_id: int
    placa: str
    marca: str
    modelo: str
    ano: int
