from fastapi import APIRouter, Depends, Query, status

from app.application.veiculo.dtos import AtualizarVeiculoInput, CriarVeiculoInput
from app.application.veiculo.use_cases import (
    AtualizarVeiculoUseCase,
    BuscarVeiculoUseCase,
    CriarVeiculoUseCase,
    ListarVeiculosUseCase,
    RemoverVeiculoUseCase,
)
from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import require_roles
from app.presentation.api.v1.veiculos.dependencies import (
    get_atualizar_veiculo_use_case,
    get_buscar_veiculo_use_case,
    get_criar_veiculo_use_case,
    get_listar_veiculos_use_case,
    get_remover_veiculo_use_case,
)
from app.presentation.api.v1.veiculos.schemas import (
    VeiculoCreateSchema,
    VeiculoSchema,
    VeiculoUpdateSchema,
)

router = APIRouter(
    prefix="/api/v1/veiculos",
    tags=["veiculos"],
    dependencies=[Depends(require_roles(Perfil.ADMIN, Perfil.ATENDENTE))],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_veiculo(
    dados: VeiculoCreateSchema,
    use_case: CriarVeiculoUseCase = Depends(get_criar_veiculo_use_case),
) -> VeiculoSchema:
    resultado = await use_case.executar(
        CriarVeiculoInput(
            cliente_id=dados.cliente_id,
            placa=dados.placa,
            marca=dados.marca,
            modelo=dados.modelo,
            ano=dados.ano,
        )
    )
    return VeiculoSchema(**vars(resultado))


@router.get("/")
async def listar_veiculos(
    cliente_id: int | None = Query(default=None),
    use_case: ListarVeiculosUseCase = Depends(get_listar_veiculos_use_case),
) -> list[VeiculoSchema]:
    resultado = await use_case.executar(cliente_id=cliente_id)
    return [VeiculoSchema(**vars(item)) for item in resultado]


@router.get("/{veiculo_id}")
async def buscar_veiculo(
    veiculo_id: int,
    use_case: BuscarVeiculoUseCase = Depends(get_buscar_veiculo_use_case),
) -> VeiculoSchema:
    resultado = await use_case.executar(veiculo_id)
    return VeiculoSchema(**vars(resultado))


@router.put("/{veiculo_id}")
async def atualizar_veiculo(
    veiculo_id: int,
    dados: VeiculoUpdateSchema,
    use_case: AtualizarVeiculoUseCase = Depends(get_atualizar_veiculo_use_case),
) -> VeiculoSchema:
    resultado = await use_case.executar(
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


@router.delete("/{veiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_veiculo(
    veiculo_id: int,
    use_case: RemoverVeiculoUseCase = Depends(get_remover_veiculo_use_case),
) -> None:
    await use_case.executar(veiculo_id)
