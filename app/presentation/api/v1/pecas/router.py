from fastapi import APIRouter, Depends, status

from app.application.peca.dtos import AtualizarPecaInput, CriarPecaInput, ReporEstoqueInput
from app.application.peca.use_cases import (
    AtualizarPecaUseCase,
    BuscarPecaUseCase,
    CriarPecaUseCase,
    ListarPecasUseCase,
    RemoverPecaUseCase,
    ReporEstoqueUseCase,
)
from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import require_roles
from app.presentation.api.v1.pecas.dependencies import (
    get_atualizar_peca_use_case,
    get_buscar_peca_use_case,
    get_criar_peca_use_case,
    get_listar_pecas_use_case,
    get_remover_peca_use_case,
    get_repor_estoque_use_case,
)
from app.presentation.api.v1.pecas.schemas import (
    PecaCreateSchema,
    PecaSchema,
    PecaUpdateSchema,
    ReporEstoqueSchema,
)

router = APIRouter(prefix="/api/v1/pecas", tags=["pecas"])

# Mesmo racional do catálogo de serviços: gestão (criar/editar/remover/repor estoque) é
# só do ADMIN; consulta é liberada a qualquer perfil autenticado (necessário para montar
# orçamento/diagnóstico de uma OS).
_apenas_admin = Depends(require_roles(Perfil.ADMIN))
_qualquer_perfil = Depends(require_roles(Perfil.ADMIN, Perfil.ATENDENTE, Perfil.MECANICO))


@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[_apenas_admin])
async def criar_peca(
    dados: PecaCreateSchema,
    use_case: CriarPecaUseCase = Depends(get_criar_peca_use_case),
) -> PecaSchema:
    resultado = await use_case.executar(
        CriarPecaInput(
            nome=dados.nome,
            descricao=dados.descricao,
            preco=dados.preco,
            quantidade_inicial=dados.quantidade_inicial,
        )
    )
    return PecaSchema(**vars(resultado))


@router.get("/", dependencies=[_qualquer_perfil])
async def listar_pecas(
    use_case: ListarPecasUseCase = Depends(get_listar_pecas_use_case),
) -> list[PecaSchema]:
    resultado = await use_case.executar()
    return [PecaSchema(**vars(item)) for item in resultado]


@router.get("/{peca_id}", dependencies=[_qualquer_perfil])
async def buscar_peca(
    peca_id: int,
    use_case: BuscarPecaUseCase = Depends(get_buscar_peca_use_case),
) -> PecaSchema:
    resultado = await use_case.executar(peca_id)
    return PecaSchema(**vars(resultado))


@router.put("/{peca_id}", dependencies=[_apenas_admin])
async def atualizar_peca(
    peca_id: int,
    dados: PecaUpdateSchema,
    use_case: AtualizarPecaUseCase = Depends(get_atualizar_peca_use_case),
) -> PecaSchema:
    resultado = await use_case.executar(
        peca_id,
        AtualizarPecaInput(nome=dados.nome, descricao=dados.descricao, preco=dados.preco),
    )
    return PecaSchema(**vars(resultado))


@router.patch("/{peca_id}/estoque", dependencies=[_apenas_admin])
async def repor_estoque(
    peca_id: int,
    dados: ReporEstoqueSchema,
    use_case: ReporEstoqueUseCase = Depends(get_repor_estoque_use_case),
) -> PecaSchema:
    resultado = await use_case.executar(peca_id, ReporEstoqueInput(quantidade=dados.quantidade))
    return PecaSchema(**vars(resultado))


@router.delete("/{peca_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[_apenas_admin])
async def remover_peca(
    peca_id: int,
    use_case: RemoverPecaUseCase = Depends(get_remover_peca_use_case),
) -> None:
    await use_case.executar(peca_id)
