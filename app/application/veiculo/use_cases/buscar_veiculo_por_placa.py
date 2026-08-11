from app.application.veiculo.dtos import VeiculoOutput
from app.application.veiculo.ports import VeiculoRepositoryProtocol
from app.domain.veiculo.exceptions import VeiculoNaoEncontradoError
from app.domain.veiculo.value_objects import Placa


class BuscarVeiculoPorPlacaUseCase:
    def __init__(self, veiculo_repository: VeiculoRepositoryProtocol) -> None:
        self._veiculo_repository = veiculo_repository

    async def executar(self, placa: str) -> VeiculoOutput:
        placa_valida = Placa(valor=placa)
        veiculo = await self._veiculo_repository.buscar_por_placa(placa_valida.valor)
        if veiculo is None:
            raise VeiculoNaoEncontradoError(placa)

        return VeiculoOutput(
            id=veiculo.id,
            cliente_id=veiculo.cliente_id,
            placa=veiculo.placa.valor,
            marca=veiculo.marca,
            modelo=veiculo.modelo,
            ano=veiculo.ano,
        )
