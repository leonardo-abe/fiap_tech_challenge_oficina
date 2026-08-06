from app.application.cliente.ports import ClienteRepositoryProtocol
from app.application.veiculo.dtos import CriarVeiculoInput, VeiculoOutput
from app.application.veiculo.ports import VeiculoRepositoryProtocol
from app.domain.cliente.exceptions import ClienteNaoEncontradoError
from app.domain.veiculo.entities import Veiculo
from app.domain.veiculo.exceptions import PlacaJaCadastradaError
from app.domain.veiculo.value_objects import Placa


class CriarVeiculoUseCase:
    def __init__(
        self,
        veiculo_repository: VeiculoRepositoryProtocol,
        cliente_repository: ClienteRepositoryProtocol,
    ) -> None:
        self._veiculo_repository = veiculo_repository
        self._cliente_repository = cliente_repository

    async def executar(self, entrada: CriarVeiculoInput) -> VeiculoOutput:
        if await self._cliente_repository.buscar_por_id(entrada.cliente_id) is None:
            raise ClienteNaoEncontradoError(entrada.cliente_id)

        placa = Placa(valor=entrada.placa)
        if await self._veiculo_repository.existe_com_placa(placa.valor):
            raise PlacaJaCadastradaError(placa.valor)

        veiculo = Veiculo(
            cliente_id=entrada.cliente_id,
            placa=placa,
            marca=entrada.marca,
            modelo=entrada.modelo,
            ano=entrada.ano,
        )
        criado = await self._veiculo_repository.criar(veiculo)

        return VeiculoOutput(
            id=criado.id,
            cliente_id=criado.cliente_id,
            placa=criado.placa.valor,
            marca=criado.marca,
            modelo=criado.modelo,
            ano=criado.ano,
        )
