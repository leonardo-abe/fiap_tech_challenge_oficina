from fastapi import APIRouter, Depends, status

from app.application.cliente.dtos import AtualizarClienteInput, CriarClienteInput
from app.application.cliente.use_cases import (
    AtualizarClienteUseCase,
    BuscarClienteUseCase,
    CriarClienteUseCase,
    ListarClientesUseCase,
    RemoverClienteUseCase,
)
from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import require_roles
from app.presentation.api.v1.clientes.dependencies import (
    get_atualizar_cliente_use_case,
    get_buscar_cliente_use_case,
    get_criar_cliente_use_case,
    get_listar_clientes_use_case,
    get_remover_cliente_use_case,
)
from app.presentation.api.v1.clientes.schemas import (
    ClienteCreateSchema,
    ClienteSchema,
    ClienteUpdateSchema,
)

router = APIRouter(
    prefix="/api/v1/clientes",
    tags=["clientes"],
    dependencies=[Depends(require_roles(Perfil.ADMIN, Perfil.ATENDENTE))],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_cliente(
    dados: ClienteCreateSchema,
    use_case: CriarClienteUseCase = Depends(get_criar_cliente_use_case),
) -> ClienteSchema:
    resultado = await use_case.executar(
        CriarClienteInput(
            nome=dados.nome, documento=dados.documento, email=dados.email, telefone=dados.telefone
        )
    )
    return ClienteSchema(**vars(resultado))


@router.get("/")
async def listar_clientes(
    use_case: ListarClientesUseCase = Depends(get_listar_clientes_use_case),
) -> list[ClienteSchema]:
    resultado = await use_case.executar()
    return [ClienteSchema(**vars(item)) for item in resultado]


@router.get("/{cliente_id}")
async def buscar_cliente(
    cliente_id: int,
    use_case: BuscarClienteUseCase = Depends(get_buscar_cliente_use_case),
) -> ClienteSchema:
    resultado = await use_case.executar(cliente_id)
    return ClienteSchema(**vars(resultado))


@router.put("/{cliente_id}")
async def atualizar_cliente(
    cliente_id: int,
    dados: ClienteUpdateSchema,
    use_case: AtualizarClienteUseCase = Depends(get_atualizar_cliente_use_case),
) -> ClienteSchema:
    resultado = await use_case.executar(
        cliente_id,
        AtualizarClienteInput(
            nome=dados.nome, documento=dados.documento, email=dados.email, telefone=dados.telefone
        ),
    )
    return ClienteSchema(**vars(resultado))


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_cliente(
    cliente_id: int,
    use_case: RemoverClienteUseCase = Depends(get_remover_cliente_use_case),
) -> None:
    await use_case.executar(cliente_id)
