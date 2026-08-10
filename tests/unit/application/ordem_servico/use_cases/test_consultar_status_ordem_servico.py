import pytest

from app.application.ordem_servico.use_cases import ConsultarStatusOrdemServicoUseCase
from app.domain.ordem_servico.entities import OrdemServico
from app.domain.ordem_servico.exceptions import OrdemServicoNaoEncontradaError
from tests.unit.application.fakes import FakeClienteRepository, FakeOrdemServicoRepository

from ._fixtures import criar_cliente_padrao


async def test_consultar_status_com_documento_correto():
    cliente_repo = FakeClienteRepository()
    ordem_repo = FakeOrdemServicoRepository()
    cliente = await criar_cliente_padrao(cliente_repo)
    ordem = await ordem_repo.criar(OrdemServico(cliente_id=cliente.id, veiculo_id=1))
    use_case = ConsultarStatusOrdemServicoUseCase(ordem_repo, cliente_repo)

    resultado = await use_case.executar(ordem.id, "11144477735")

    assert resultado.id == ordem.id


async def test_consultar_status_ordem_inexistente_levanta_erro():
    use_case = ConsultarStatusOrdemServicoUseCase(
        FakeOrdemServicoRepository(), FakeClienteRepository()
    )

    with pytest.raises(OrdemServicoNaoEncontradaError):
        await use_case.executar(999, "11144477735")


async def test_consultar_status_com_documento_incorreto_levanta_erro():
    cliente_repo = FakeClienteRepository()
    ordem_repo = FakeOrdemServicoRepository()
    cliente = await criar_cliente_padrao(cliente_repo)
    ordem = await ordem_repo.criar(OrdemServico(cliente_id=cliente.id, veiculo_id=1))
    use_case = ConsultarStatusOrdemServicoUseCase(ordem_repo, cliente_repo)

    with pytest.raises(OrdemServicoNaoEncontradaError):
        await use_case.executar(ordem.id, "52998224725")


async def test_consultar_status_com_documento_de_formato_invalido_levanta_ordem_nao_encontrada():
    # ID-004: documento mal formado (dígito verificador inválido) não pode propagar como
    # DocumentoInvalidoError (422) - isso distinguiria de OrdemServicoNaoEncontradaError
    # (404) e permitiria enumerar ordem_id existentes sem nunca precisar de um documento
    # válido, só observando a diferença de status HTTP entre os dois casos.
    cliente_repo = FakeClienteRepository()
    ordem_repo = FakeOrdemServicoRepository()
    cliente = await criar_cliente_padrao(cliente_repo)
    ordem = await ordem_repo.criar(OrdemServico(cliente_id=cliente.id, veiculo_id=1))
    use_case = ConsultarStatusOrdemServicoUseCase(ordem_repo, cliente_repo)

    with pytest.raises(OrdemServicoNaoEncontradaError):
        await use_case.executar(ordem.id, "123")
