from app.application.cliente.ports import ClienteRepositoryProtocol
from app.application.ordem_servico.dtos import StatusOrdemServicoOutput
from app.application.ordem_servico.ports import OrdemServicoRepositoryProtocol
from app.domain.cliente.exceptions import DocumentoInvalidoError
from app.domain.cliente.value_objects import Documento
from app.domain.ordem_servico.exceptions import OrdemServicoNaoEncontradaError


class ConsultarStatusOrdemServicoUseCase:
    def __init__(
        self,
        ordem_servico_repository: OrdemServicoRepositoryProtocol,
        cliente_repository: ClienteRepositoryProtocol,
    ) -> None:
        self._ordem_servico_repository = ordem_servico_repository
        self._cliente_repository = cliente_repository

    async def executar(self, ordem_id: int, documento: str) -> StatusOrdemServicoOutput:
        ordem = await self._ordem_servico_repository.buscar_por_id(ordem_id)
        if ordem is None:
            raise OrdemServicoNaoEncontradaError(ordem_id)

        cliente = await self._cliente_repository.buscar_por_id(ordem.cliente_id)

        # documento que não corresponde ao cliente da OS - incluindo um documento com
        # formato/dígito verificador inválido - é tratado como "não encontrada" (404).
        # A consulta pública não deve revelar a um estranho se aquele id de OS existe:
        # deixar DocumentoInvalidoError propagar (422) diferenciaria "OS existe, documento
        # mal formado" de "OS não existe" (404), o que por si só já vaza a existência da OS
        # para quem tentar qualquer id sem precisar acertar um documento válido.
        documento_confere = False
        if cliente is not None:
            try:
                documento_confere = cliente.documento == Documento(valor=documento)
            except DocumentoInvalidoError:
                documento_confere = False

        if not documento_confere:
            raise OrdemServicoNaoEncontradaError(ordem_id)

        return StatusOrdemServicoOutput(
            id=ordem.id,
            status=ordem.status.value,
            recebida_em=ordem.recebida_em,
            execucao_iniciada_em=ordem.execucao_iniciada_em,
            finalizada_em=ordem.finalizada_em,
        )
