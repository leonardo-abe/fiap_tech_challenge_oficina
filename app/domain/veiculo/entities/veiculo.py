from dataclasses import dataclass

from app.domain.veiculo.value_objects import Placa


@dataclass
class Veiculo:
    cliente_id: int
    placa: Placa
    marca: str
    modelo: str
    ano: int
    id: int | None = None
