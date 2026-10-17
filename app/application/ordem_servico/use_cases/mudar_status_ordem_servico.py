from app.application.cliente.ports import ClienteRepositoryProtocol
from app.application.ordem_servico.dtos import OrdemServicoOutput
from app.application.ordem_servico.mappers import ordem_servico_to_output
from app.application.ordem_servico.ports import (
    NotificadorOrcamentoProtocol,
    OrdemServicoRepositoryProtocol,
)
from app.application.peca.ports import PecaRepositoryProtocol
from app.domain.ordem_servico.exceptions import OrdemServicoNaoEncontradaError
from app.domain.ordem_servico.value_objects import StatusOS

_STATUS_COM_ESTORNO_DE_ESTOQUE = frozenset({StatusOS.REPROVADA, StatusOS.CANCELADA})


class MudarStatusOrdemServicoUseCase:
    def __init__(
        self,
        ordem_servico_repository: OrdemServicoRepositoryProtocol,
        peca_repository: PecaRepositoryProtocol,
        cliente_repository: ClienteRepositoryProtocol,
        notificador: NotificadorOrcamentoProtocol,
    ) -> None:
        self._ordem_servico_repository = ordem_servico_repository
        self._peca_repository = peca_repository
        self._cliente_repository = cliente_repository
        self._notificador = notificador

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
        resultado = ordem_servico_to_output(atualizada)

        # notifica o cliente a cada transição de status; se o cliente não for encontrado
        # (não deveria acontecer em operação normal) ou o envio falhar, a transição já
        # está persistida e não deve ser revertida por um problema de notificação.
        cliente = await self._cliente_repository.buscar_por_id(atualizada.cliente_id)
        if cliente is not None:
            await self._notificador.notificar_mudanca_status(
                destinatario_nome=cliente.nome,
                destinatario_email=cliente.email,
                ordem=resultado,
            )

        return resultado
