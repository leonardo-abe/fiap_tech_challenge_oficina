from dataclasses import dataclass


@dataclass(frozen=True)
class RelatorioTempoMedioExecucaoOutput:
    quantidade_ordens_finalizadas: int
    tempo_medio_execucao_horas: float | None
