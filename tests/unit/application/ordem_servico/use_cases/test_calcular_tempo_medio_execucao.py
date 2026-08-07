from datetime import UTC, datetime, timedelta

from app.application.ordem_servico.use_cases import CalcularTempoMedioExecucaoUseCase
from app.domain.ordem_servico.entities import OrdemServico
from app.domain.ordem_servico.value_objects import StatusOS
from tests.unit.application.fakes import FakeOrdemServicoRepository


async def test_calcular_tempo_medio_execucao_sem_ordens():
    resultado = await CalcularTempoMedioExecucaoUseCase(FakeOrdemServicoRepository()).executar()

    assert resultado.quantidade_ordens_finalizadas == 0
    assert resultado.tempo_medio_execucao_horas is None


async def test_calcular_tempo_medio_execucao_ignora_ordens_sem_execucao():
    repositorio = FakeOrdemServicoRepository()
    await repositorio.criar(OrdemServico(cliente_id=1, veiculo_id=1, status=StatusOS.RECEBIDA))

    resultado = await CalcularTempoMedioExecucaoUseCase(repositorio).executar()

    assert resultado.quantidade_ordens_finalizadas == 0


async def test_calcular_tempo_medio_execucao_com_ordens_finalizadas():
    base = datetime.now(UTC)
    repositorio = FakeOrdemServicoRepository()
    await repositorio.criar(
        OrdemServico(
            cliente_id=1,
            veiculo_id=1,
            status=StatusOS.ENTREGUE,
            execucao_iniciada_em=base,
            finalizada_em=base + timedelta(hours=2),
        )
    )
    await repositorio.criar(
        OrdemServico(
            cliente_id=1,
            veiculo_id=1,
            status=StatusOS.ENTREGUE,
            execucao_iniciada_em=base,
            finalizada_em=base + timedelta(hours=4),
        )
    )

    resultado = await CalcularTempoMedioExecucaoUseCase(repositorio).executar()

    assert resultado.quantidade_ordens_finalizadas == 2
    assert resultado.tempo_medio_execucao_horas == 3.0
