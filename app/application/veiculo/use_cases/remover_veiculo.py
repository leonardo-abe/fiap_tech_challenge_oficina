from app.application.veiculo.ports import VeiculoRepositoryProtocol
from app.domain.veiculo.exceptions import VeiculoNaoEncontradoError


class RemoverVeiculoUseCase:
    def __init__(self, veiculo_repository: VeiculoRepositoryProtocol) -> None:
        self._veiculo_repository = veiculo_repository

    async def executar(self, veiculo_id: int) -> None:
        veiculo = await self._veiculo_repository.buscar_por_id(veiculo_id)
        if veiculo is None:
            raise VeiculoNaoEncontradoError(veiculo_id)

        await self._veiculo_repository.remover(veiculo_id)
