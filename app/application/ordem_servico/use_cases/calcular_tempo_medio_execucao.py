from app.application.ordem_servico.dtos import RelatorioTempoMedioExecucaoOutput
from app.application.ordem_servico.ports import OrdemServicoRepositoryProtocol


class CalcularTempoMedioExecucaoUseCase:
    def __init__(self, ordem_servico_repository: OrdemServicoRepositoryProtocol) -> None:
        self._ordem_servico_repository = ordem_servico_repository

    async def executar(self) -> RelatorioTempoMedioExecucaoOutput:
        ordens = await self._ordem_servico_repository.listar()

        duracoes = [
            ordem.finalizada_em - ordem.execucao_iniciada_em
            for ordem in ordens
            if ordem.execucao_iniciada_em is not None and ordem.finalizada_em is not None
        ]

        if not duracoes:
            return RelatorioTempoMedioExecucaoOutput(
                quantidade_ordens_finalizadas=0, tempo_medio_execucao_horas=None
            )

        media_segundos = sum(duracao.total_seconds() for duracao in duracoes) / len(duracoes)

        return RelatorioTempoMedioExecucaoOutput(
            quantidade_ordens_finalizadas=len(duracoes),
            tempo_medio_execucao_horas=media_segundos / 3600,
        )
