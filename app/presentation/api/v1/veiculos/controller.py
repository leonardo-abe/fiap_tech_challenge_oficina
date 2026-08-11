from app.application.veiculo.dtos import AtualizarVeiculoInput, CriarVeiculoInput
from app.application.veiculo.use_cases import (
    AtualizarVeiculoUseCase,
    BuscarVeiculoPorPlacaUseCase,
    BuscarVeiculoUseCase,
    CriarVeiculoUseCase,
    ListarVeiculosUseCase,
    RemoverVeiculoUseCase,
)
from app.presentation.api.v1.veiculos.schemas import (
    VeiculoCreateSchema,
    VeiculoSchema,
    VeiculoUpdateSchema,
)


class VeiculoController:
    def __init__(
        self,
        criar_use_case: CriarVeiculoUseCase,
        atualizar_use_case: AtualizarVeiculoUseCase,
        buscar_use_case: BuscarVeiculoUseCase,
        buscar_por_placa_use_case: BuscarVeiculoPorPlacaUseCase,
        listar_use_case: ListarVeiculosUseCase,
        remover_use_case: RemoverVeiculoUseCase,
    ) -> None:
        self._criar_use_case = criar_use_case
        self._atualizar_use_case = atualizar_use_case
        self._buscar_use_case = buscar_use_case
        self._buscar_por_placa_use_case = buscar_por_placa_use_case
        self._listar_use_case = listar_use_case
        self._remover_use_case = remover_use_case

    async def criar(self, dados: VeiculoCreateSchema) -> VeiculoSchema:
        resultado = await self._criar_use_case.executar(
            CriarVeiculoInput(
                cliente_id=dados.cliente_id,
                placa=dados.placa,
                marca=dados.marca,
                modelo=dados.modelo,
                ano=dados.ano,
            )
        )
        return VeiculoSchema(**vars(resultado))

    async def listar(
        self, cliente_id: int | None, limit: int = 50, offset: int = 0
    ) -> list[VeiculoSchema]:
        resultado = await self._listar_use_case.executar(
            cliente_id=cliente_id, limit=limit, offset=offset
        )
        return [VeiculoSchema(**vars(item)) for item in resultado]

    async def buscar(self, veiculo_id: int) -> VeiculoSchema:
        resultado = await self._buscar_use_case.executar(veiculo_id)
        return VeiculoSchema(**vars(resultado))

    async def buscar_por_placa(self, placa: str) -> VeiculoSchema:
        resultado = await self._buscar_por_placa_use_case.executar(placa)
        return VeiculoSchema(**vars(resultado))

    async def atualizar(self, veiculo_id: int, dados: VeiculoUpdateSchema) -> VeiculoSchema:
        resultado = await self._atualizar_use_case.executar(
            veiculo_id,
            AtualizarVeiculoInput(
                cliente_id=dados.cliente_id,
                placa=dados.placa,
                marca=dados.marca,
                modelo=dados.modelo,
                ano=dados.ano,
            ),
        )
        return VeiculoSchema(**vars(resultado))

    async def remover(self, veiculo_id: int) -> None:
        await self._remover_use_case.executar(veiculo_id)
