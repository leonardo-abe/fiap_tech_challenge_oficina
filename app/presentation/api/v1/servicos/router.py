from fastapi import APIRouter, Depends, status

from app.application.servico.dtos import AtualizarServicoInput, CriarServicoInput
from app.application.servico.use_cases import (
    AtualizarServicoUseCase,
    BuscarServicoUseCase,
    CriarServicoUseCase,
    ListarServicosUseCase,
    RemoverServicoUseCase,
)
from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import require_roles
from app.presentation.api.v1.servicos.dependencies import (
    get_atualizar_servico_use_case,
    get_buscar_servico_use_case,
    get_criar_servico_use_case,
    get_listar_servicos_use_case,
    get_remover_servico_use_case,
)
from app.presentation.api.v1.servicos.schemas import (
    ServicoCreateSchema,
    ServicoSchema,
    ServicoUpdateSchema,
)

router = APIRouter(prefix="/api/v1/servicos", tags=["servicos"])

# Gestão do catálogo (criar/editar/remover) é só do ADMIN; consulta é liberada para
# qualquer perfil autenticado, pois atendente e mecânico precisam ver o catálogo para
# montar orçamento/diagnóstico de uma OS.
_apenas_admin = Depends(require_roles(Perfil.ADMIN))
_qualquer_perfil = Depends(require_roles(Perfil.ADMIN, Perfil.ATENDENTE, Perfil.MECANICO))


@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[_apenas_admin])
async def criar_servico(
    dados: ServicoCreateSchema,
    use_case: CriarServicoUseCase = Depends(get_criar_servico_use_case),
) -> ServicoSchema:
    resultado = await use_case.executar(
        CriarServicoInput(nome=dados.nome, descricao=dados.descricao, preco=dados.preco)
    )
    return ServicoSchema(**vars(resultado))


@router.get("/", dependencies=[_qualquer_perfil])
async def listar_servicos(
    use_case: ListarServicosUseCase = Depends(get_listar_servicos_use_case),
) -> list[ServicoSchema]:
    resultado = await use_case.executar()
    return [ServicoSchema(**vars(item)) for item in resultado]


@router.get("/{servico_id}", dependencies=[_qualquer_perfil])
async def buscar_servico(
    servico_id: int,
    use_case: BuscarServicoUseCase = Depends(get_buscar_servico_use_case),
) -> ServicoSchema:
    resultado = await use_case.executar(servico_id)
    return ServicoSchema(**vars(resultado))


@router.put("/{servico_id}", dependencies=[_apenas_admin])
async def atualizar_servico(
    servico_id: int,
    dados: ServicoUpdateSchema,
    use_case: AtualizarServicoUseCase = Depends(get_atualizar_servico_use_case),
) -> ServicoSchema:
    resultado = await use_case.executar(
        servico_id,
        AtualizarServicoInput(nome=dados.nome, descricao=dados.descricao, preco=dados.preco),
    )
    return ServicoSchema(**vars(resultado))


@router.delete(
    "/{servico_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[_apenas_admin]
)
async def remover_servico(
    servico_id: int,
    use_case: RemoverServicoUseCase = Depends(get_remover_servico_use_case),
) -> None:
    await use_case.executar(servico_id)
