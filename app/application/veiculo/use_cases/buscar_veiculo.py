from app.application.veiculo.dtos import VeiculoOutput
from app.application.veiculo.ports import VeiculoRepositoryProtocol
from app.domain.veiculo.exceptions import VeiculoNaoEncontradoError


class BuscarVeiculoUseCase:
    def __init__(self, veiculo_repository: VeiculoRepositoryProtocol) -> None:
        self._veiculo_repository = veiculo_repository

    async def executar(self, veiculo_id: int) -> VeiculoOutput:
        veiculo = await self._veiculo_repository.buscar_por_id(veiculo_id)
        if veiculo is None:
            raise VeiculoNaoEncontradoError(veiculo_id)

        return VeiculoOutput(
            id=veiculo.id,
            cliente_id=veiculo.cliente_id,
            placa=veiculo.placa.valor,
            marca=veiculo.marca,
            modelo=veiculo.modelo,
            ano=veiculo.ano,
        )
