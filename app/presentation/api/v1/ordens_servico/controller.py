from app.application.ordem_servico.dtos import (
    CriarOrdemServicoInput,
    ItemPecaInput,
    ItemServicoInput,
)
from app.application.ordem_servico.use_cases import (
    BuscarOrdemServicoUseCase,
    CalcularTempoMedioExecucaoUseCase,
    ConsultarStatusOrdemServicoUseCase,
    CriarOrdemServicoUseCase,
    GerarOrcamentoUseCase,
    ListarOrdensServicoUseCase,
    MudarStatusOrdemServicoUseCase,
)
from app.domain.ordem_servico.value_objects import StatusOS
from app.presentation.api.v1.ordens_servico.schemas import (
    OrdemServicoCreateSchema,
    OrdemServicoSchema,
    OrdemServicoStatusSchema,
    RelatorioTempoMedioExecucaoSchema,
)


class OrdemServicoController:
    def __init__(
        self,
        criar_use_case: CriarOrdemServicoUseCase,
        mudar_status_use_case: MudarStatusOrdemServicoUseCase,
        gerar_orcamento_use_case: GerarOrcamentoUseCase,
        listar_use_case: ListarOrdensServicoUseCase,
        buscar_use_case: BuscarOrdemServicoUseCase,
        consultar_status_use_case: ConsultarStatusOrdemServicoUseCase,
        calcular_tempo_medio_execucao_use_case: CalcularTempoMedioExecucaoUseCase,
    ) -> None:
        self._criar_use_case = criar_use_case
        self._mudar_status_use_case = mudar_status_use_case
        self._gerar_orcamento_use_case = gerar_orcamento_use_case
        self._listar_use_case = listar_use_case
        self._buscar_use_case = buscar_use_case
        self._consultar_status_use_case = consultar_status_use_case
        self._calcular_tempo_medio_execucao_use_case = calcular_tempo_medio_execucao_use_case

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
        resultado = await self._gerar_orcamento_use_case.executar(ordem_id)
        return OrdemServicoSchema.model_validate(resultado)

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

    async def listar(self, limit: int = 50, offset: int = 0) -> list[OrdemServicoSchema]:
        resultado = await self._listar_use_case.executar(limit=limit, offset=offset)
        return [OrdemServicoSchema.model_validate(item) for item in resultado]

    async def buscar(self, ordem_id: int) -> OrdemServicoSchema:
        resultado = await self._buscar_use_case.executar(ordem_id)
        return OrdemServicoSchema.model_validate(resultado)

    async def consultar_status(self, ordem_id: int, documento: str) -> OrdemServicoStatusSchema:
        resultado = await self._consultar_status_use_case.executar(ordem_id, documento)
        return OrdemServicoStatusSchema.model_validate(resultado)

    async def relatorio_tempo_medio_execucao(self) -> RelatorioTempoMedioExecucaoSchema:
        resultado = await self._calcular_tempo_medio_execucao_use_case.executar()
        return RelatorioTempoMedioExecucaoSchema.model_validate(resultado)
