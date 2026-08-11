from app.application.veiculo.dtos import VeiculoOutput
from app.application.veiculo.ports import VeiculoRepositoryProtocol


class ListarVeiculosUseCase:
    def __init__(self, veiculo_repository: VeiculoRepositoryProtocol) -> None:
        self._veiculo_repository = veiculo_repository

    async def executar(
        self, cliente_id: int | None = None, limit: int = 50, offset: int = 0
    ) -> list[VeiculoOutput]:
        veiculos = await self._veiculo_repository.listar(
            cliente_id=cliente_id, limit=limit, offset=offset
        )

        return [
            VeiculoOutput(
                id=veiculo.id,
                cliente_id=veiculo.cliente_id,
                placa=veiculo.placa.valor,
                marca=veiculo.marca,
                modelo=veiculo.modelo,
                ano=veiculo.ano,
            )
            for veiculo in veiculos
        ]
