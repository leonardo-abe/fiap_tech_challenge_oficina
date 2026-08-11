from app.application.cliente.ports import ClienteRepositoryProtocol
from app.application.ordem_servico.dtos import OrdemServicoOutput
from app.application.ordem_servico.mappers import ordem_servico_to_output
from app.application.ordem_servico.ports import (
    NotificadorOrcamentoProtocol,
    OrdemServicoRepositoryProtocol,
)
from app.domain.cliente.exceptions import ClienteNaoEncontradoError
from app.domain.ordem_servico.exceptions import OrdemServicoNaoEncontradaError
from app.domain.ordem_servico.value_objects import StatusOS


class GerarOrcamentoUseCase:
    def __init__(
        self,
        ordem_servico_repository: OrdemServicoRepositoryProtocol,
        cliente_repository: ClienteRepositoryProtocol,
        notificador: NotificadorOrcamentoProtocol,
    ) -> None:
        self._ordem_servico_repository = ordem_servico_repository
        self._cliente_repository = cliente_repository
        self._notificador = notificador

    async def executar(self, ordem_id: int) -> OrdemServicoOutput:
        ordem = await self._ordem_servico_repository.buscar_por_id(ordem_id)
        if ordem is None:
            raise OrdemServicoNaoEncontradaError(ordem_id)

        cliente = await self._cliente_repository.buscar_por_id(ordem.cliente_id)
        if cliente is None:
            raise ClienteNaoEncontradoError(ordem.cliente_id)

        ordem.mudar_status(StatusOS.AGUARDANDO_APROVACAO)
        atualizada = await self._ordem_servico_repository.atualizar(ordem)
        resultado = ordem_servico_to_output(atualizada)

        # a notificação acontece depois da transição já persistida - se o envio falhar
        # (SMTP fora do ar, etc.), a OS já está em AGUARDANDO_APROVACAO e pode ser
        # reconsultada/reenviada, em vez de a ação inteira falhar por um problema de terceiro.
        await self._notificador.notificar_orcamento_gerado(
            destinatario_nome=cliente.nome,
            destinatario_email=cliente.email,
            ordem=resultado,
        )

        return resultado
