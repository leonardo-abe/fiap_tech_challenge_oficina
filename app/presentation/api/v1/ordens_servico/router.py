from fastapi import APIRouter, Depends, Query, status

from app.domain.usuario.value_objects import Perfil
from app.presentation.api.v1.auth.dependencies import require_roles
from app.presentation.api.v1.ordens_servico.controller import OrdemServicoController
from app.presentation.api.v1.ordens_servico.dependencies import get_ordem_servico_controller
from app.presentation.api.v1.ordens_servico.schemas import (
    OrdemServicoCreateSchema,
    OrdemServicoSchema,
    OrdemServicoStatusSchema,
)

router = APIRouter(prefix="/api/v1/ordens-servico", tags=["ordens-servico"])

# Permissões seguem a tabela do desafio: diagnóstico/execução são do MECANICO,
# aprovação de orçamento/entrega/cancelamento são do ATENDENTE, ADMIN pode tudo.
# Consulta administrativa é liberada a qualquer perfil autenticado; a consulta por
# status (GET /{ordem_id}/status) é a única rota pública, sem JWT - o desafio só exige
# autenticação para as APIs administrativas.
_admin_atendente = Depends(require_roles(Perfil.ADMIN, Perfil.ATENDENTE))
_admin_mecanico = Depends(require_roles(Perfil.ADMIN, Perfil.MECANICO))
_qualquer_perfil = Depends(require_roles(Perfil.ADMIN, Perfil.ATENDENTE, Perfil.MECANICO))


@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[_admin_atendente])
async def criar_ordem_servico(
    dados: OrdemServicoCreateSchema,
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> OrdemServicoSchema:
    return await controller.criar(dados)


@router.post("/{ordem_id}/diagnostico", dependencies=[_admin_mecanico])
async def iniciar_diagnostico(
    ordem_id: int,
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> OrdemServicoSchema:
    return await controller.iniciar_diagnostico(ordem_id)


@router.post("/{ordem_id}/orcamento/gerar", dependencies=[_admin_mecanico])
async def gerar_orcamento(
    ordem_id: int,
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> OrdemServicoSchema:
    return await controller.gerar_orcamento(ordem_id)


@router.post("/{ordem_id}/orcamento/aprovar", dependencies=[_admin_atendente])
async def aprovar_orcamento(
    ordem_id: int,
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> OrdemServicoSchema:
    return await controller.aprovar_orcamento(ordem_id)


@router.post("/{ordem_id}/orcamento/reprovar", dependencies=[_admin_atendente])
async def reprovar_orcamento(
    ordem_id: int,
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> OrdemServicoSchema:
    return await controller.reprovar_orcamento(ordem_id)


@router.post("/{ordem_id}/execucao/finalizar", dependencies=[_admin_mecanico])
async def finalizar_execucao(
    ordem_id: int,
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> OrdemServicoSchema:
    return await controller.finalizar_execucao(ordem_id)


@router.post("/{ordem_id}/entrega", dependencies=[_admin_atendente])
async def entregar_ordem_servico(
    ordem_id: int,
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> OrdemServicoSchema:
    return await controller.entregar(ordem_id)


@router.post("/{ordem_id}/cancelamento", dependencies=[_admin_atendente])
async def cancelar_ordem_servico(
    ordem_id: int,
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> OrdemServicoSchema:
    return await controller.cancelar(ordem_id)


@router.get("/", dependencies=[_qualquer_perfil])
async def listar_ordens_servico(
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> list[OrdemServicoSchema]:
    return await controller.listar()


@router.get("/{ordem_id}", dependencies=[_qualquer_perfil])
async def buscar_ordem_servico(
    ordem_id: int,
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> OrdemServicoSchema:
    return await controller.buscar(ordem_id)


@router.get("/{ordem_id}/status")
async def consultar_status_ordem_servico(
    ordem_id: int,
    documento: str = Query(..., description="CPF ou CNPJ do cliente dono da OS"),
    controller: OrdemServicoController = Depends(get_ordem_servico_controller),
) -> OrdemServicoStatusSchema:
    return await controller.consultar_status(ordem_id, documento)
