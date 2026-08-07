from app.application.ordem_servico.dtos import (
    CriarOrdemServicoInput,
    ItemPecaInput,
    ItemServicoInput,
)
from app.application.ordem_servico.use_cases import (
    CriarOrdemServicoUseCase,
    MudarStatusOrdemServicoUseCase,
)
from app.domain.ordem_servico.value_objects import StatusOS
from app.presentation.api.v1.ordens_servico.schemas import (
    OrdemServicoCreateSchema,
    OrdemServicoSchema,
)


class OrdemServicoController:
    def __init__(
        self,
        criar_use_case: CriarOrdemServicoUseCase,
        mudar_status_use_case: MudarStatusOrdemServicoUseCase,
    ) -> None:
        self._criar_use_case = criar_use_case
        self._mudar_status_use_case = mudar_status_use_case

    async def criar(self, dados: OrdemServicoCreateSchema) -> OrdemServicoSchema:
        resultado = await self._criar_use_case.executar(
            CriarOrdemServicoInput(
                cliente_id=dados.cliente_id,
                veiculo_id=dados.veiculo_id,
                itens_servico=[
                    ItemServicoInput(servico_id=item.servico_id) for item in dados.itens_servico
                ],
                itens_peca=[
                    ItemPecaInput(peca_id=item.peca_id, quantidade=item.quantidade)
                    for item in dados.itens_peca
                ],
            )
        )
        return OrdemServicoSchema.model_validate(resultado)

    async def iniciar_diagnostico(self, ordem_id: int) -> OrdemServicoSchema:
        return await self._mudar_status(ordem_id, StatusOS.EM_DIAGNOSTICO)

    async def gerar_orcamento(self, ordem_id: int) -> OrdemServicoSchema:
        return await self._mudar_status(ordem_id, StatusOS.AGUARDANDO_APROVACAO)

    async def aprovar_orcamento(self, ordem_id: int) -> OrdemServicoSchema:
        return await self._mudar_status(ordem_id, StatusOS.EM_EXECUCAO)

    async def reprovar_orcamento(self, ordem_id: int) -> OrdemServicoSchema:
        return await self._mudar_status(ordem_id, StatusOS.REPROVADA)

    async def finalizar_execucao(self, ordem_id: int) -> OrdemServicoSchema:
        return await self._mudar_status(ordem_id, StatusOS.FINALIZADA)

    async def entregar(self, ordem_id: int) -> OrdemServicoSchema:
        return await self._mudar_status(ordem_id, StatusOS.ENTREGUE)

    async def cancelar(self, ordem_id: int) -> OrdemServicoSchema:
        return await self._mudar_status(ordem_id, StatusOS.CANCELADA)

    async def _mudar_status(self, ordem_id: int, novo_status: StatusOS) -> OrdemServicoSchema:
        resultado = await self._mudar_status_use_case.executar(ordem_id, novo_status)
        return OrdemServicoSchema.model_validate(resultado)
