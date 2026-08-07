from app.application.ordem_servico.use_cases import ListarOrdensServicoUseCase
from app.domain.ordem_servico.entities import OrdemServico
from tests.unit.application.fakes import FakeOrdemServicoRepository


async def test_listar_ordens_servico_vazio():
    resultado = await ListarOrdensServicoUseCase(FakeOrdemServicoRepository()).executar()

    assert resultado == []


async def test_listar_ordens_servico_com_registros():
    repositorio = FakeOrdemServicoRepository()
    await repositorio.criar(OrdemServico(cliente_id=1, veiculo_id=1))
    await repositorio.criar(OrdemServico(cliente_id=2, veiculo_id=2))

    resultado = await ListarOrdensServicoUseCase(repositorio).executar()

    assert len(resultado) == 2
