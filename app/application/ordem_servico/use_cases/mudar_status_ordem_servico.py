from app.application.ordem_servico.dtos import OrdemServicoOutput
from app.application.ordem_servico.mappers import ordem_servico_to_output
from app.application.ordem_servico.ports import OrdemServicoRepositoryProtocol
from app.application.peca.ports import PecaRepositoryProtocol
from app.domain.ordem_servico.exceptions import OrdemServicoNaoEncontradaError
from app.domain.ordem_servico.value_objects import StatusOS

_STATUS_COM_ESTORNO_DE_ESTOQUE = frozenset({StatusOS.REPROVADA, StatusOS.CANCELADA})


class MudarStatusOrdemServicoUseCase:
    def __init__(
        self,
        ordem_servico_repository: OrdemServicoRepositoryProtocol,
        peca_repository: PecaRepositoryProtocol,
    ) -> None:
        self._ordem_servico_repository = ordem_servico_repository
        self._peca_repository = peca_repository

    async def executar(self, ordem_id: int, novo_status: StatusOS) -> OrdemServicoOutput:
        ordem = await self._ordem_servico_repository.buscar_por_id(ordem_id)
        if ordem is None:
            raise OrdemServicoNaoEncontradaError(ordem_id)

        ordem.mudar_status(novo_status)

        if novo_status in _STATUS_COM_ESTORNO_DE_ESTOQUE:
            # a baixa de estoque das peças acontece na criação da OS (antes de qualquer
            # decisão do cliente); se a OS termina sem execução, o estoque reservado
            # precisa voltar - senão fica "preso" para sempre no agregado Peca.
            for item in ordem.itens_peca:
                await self._peca_repository.incrementar_estoque(item.peca_id, item.quantidade)

        atualizada = await self._ordem_servico_repository.atualizar(ordem)

        return ordem_servico_to_output(atualizada)
