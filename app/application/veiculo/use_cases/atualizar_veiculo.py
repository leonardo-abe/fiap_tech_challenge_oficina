from app.application.cliente.ports import ClienteRepositoryProtocol
from app.application.veiculo.dtos import AtualizarVeiculoInput, VeiculoOutput
from app.application.veiculo.ports import VeiculoRepositoryProtocol
from app.domain.cliente.exceptions import ClienteNaoEncontradoError
from app.domain.veiculo.exceptions import PlacaJaCadastradaError, VeiculoNaoEncontradoError
from app.domain.veiculo.value_objects import Placa


class AtualizarVeiculoUseCase:
    def __init__(
        self,
        veiculo_repository: VeiculoRepositoryProtocol,
        cliente_repository: ClienteRepositoryProtocol,
    ) -> None:
        self._veiculo_repository = veiculo_repository
        self._cliente_repository = cliente_repository

    async def executar(self, veiculo_id: int, entrada: AtualizarVeiculoInput) -> VeiculoOutput:
        veiculo = await self._veiculo_repository.buscar_por_id(veiculo_id)
        if veiculo is None:
            raise VeiculoNaoEncontradoError(veiculo_id)

        if await self._cliente_repository.buscar_por_id(entrada.cliente_id) is None:
            raise ClienteNaoEncontradoError(entrada.cliente_id)

        placa = Placa(valor=entrada.placa)
        placa_mudou = placa.valor != veiculo.placa.valor
        if placa_mudou and await self._veiculo_repository.existe_com_placa(placa.valor):
            raise PlacaJaCadastradaError(placa.valor)

        veiculo.cliente_id = entrada.cliente_id
        veiculo.placa = placa
        veiculo.marca = entrada.marca
        veiculo.modelo = entrada.modelo
        veiculo.ano = entrada.ano
        atualizado = await self._veiculo_repository.atualizar(veiculo)

        return VeiculoOutput(
            id=atualizado.id,
            cliente_id=atualizado.cliente_id,
            placa=atualizado.placa.valor,
            marca=atualizado.marca,
            modelo=atualizado.modelo,
            ano=atualizado.ano,
        )
