from app.application.cliente.ports import ClienteRepositoryProtocol
from app.application.ordem_servico.dtos import OrdemServicoOutput
from app.application.ordem_servico.ports import OrdemServicoRepositoryProtocol
from app.application.ordem_servico.use_cases.mudar_status_ordem_servico import (
    MudarStatusOrdemServicoUseCase,
)
from app.domain.cliente.exceptions import DocumentoInvalidoError
from app.domain.cliente.value_objects import Documento
from app.domain.ordem_servico.exceptions import OrdemServicoNaoEncontradaError
from app.domain.ordem_servico.value_objects import StatusOS


class DecidirOrcamentoExternoUseCase:
    """Permite ao próprio cliente aprovar/recusar o orçamento sem autenticação de
    funcionário - a "posse" da OS é comprovada pelo documento (CPF/CNPJ), igual à
    consulta pública de status (ConsultarStatusOrdemServicoUseCase)."""

    def __init__(
        self,
        ordem_servico_repository: OrdemServicoRepositoryProtocol,
        cliente_repository: ClienteRepositoryProtocol,
        mudar_status_use_case: MudarStatusOrdemServicoUseCase,
    ) -> None:
        self._ordem_servico_repository = ordem_servico_repository
        self._cliente_repository = cliente_repository
        self._mudar_status_use_case = mudar_status_use_case

    async def executar(self, ordem_id: int, documento: str, aprovar: bool) -> OrdemServicoOutput:
        ordem = await self._ordem_servico_repository.buscar_por_id(ordem_id)
        if ordem is None:
            raise OrdemServicoNaoEncontradaError(ordem_id)

        cliente = await self._cliente_repository.buscar_por_id(ordem.cliente_id)

        # mesmo cuidado anti-enumeração da consulta pública de status: documento que não
        # confere (ou mal formado) vira 404, nunca 403/422 - senão um estranho distingue
        # "OS existe" de "OS não existe" só testando ids, sem precisar de documento válido.
        documento_confere = False
        if cliente is not None:
            try:
                documento_confere = cliente.documento == Documento(valor=documento)
            except DocumentoInvalidoError:
                documento_confere = False

        if not documento_confere:
            raise OrdemServicoNaoEncontradaError(ordem_id)

        novo_status = StatusOS.EM_EXECUCAO if aprovar else StatusOS.REPROVADA
        return await self._mudar_status_use_case.executar(ordem_id, novo_status)
