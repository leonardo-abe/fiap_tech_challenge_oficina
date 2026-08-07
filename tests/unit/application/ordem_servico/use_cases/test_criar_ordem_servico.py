import pytest

from app.application.ordem_servico.dtos import (
    CriarOrdemServicoInput,
    ItemPecaInput,
    ItemServicoInput,
)
from app.application.ordem_servico.use_cases import CriarOrdemServicoUseCase
from app.domain.cliente.entities import Cliente
from app.domain.cliente.exceptions import ClienteNaoEncontradoError
from app.domain.cliente.value_objects import Documento
from app.domain.ordem_servico.exceptions import (
    OrdemServicoSemItensError,
    VeiculoNaoPertenceAoClienteError,
)
from app.domain.peca.exceptions import EstoqueInsuficienteError, PecaNaoEncontradaError
from app.domain.servico.exceptions import ServicoNaoEncontradoError
from app.domain.veiculo.exceptions import VeiculoNaoEncontradoError
from tests.unit.application.fakes import (
    FakeClienteRepository,
    FakeOrdemServicoRepository,
    FakePecaRepository,
    FakeServicoRepository,
    FakeVeiculoRepository,
)

from ._fixtures import (
    criar_cliente_padrao,
    criar_peca_padrao,
    criar_servico_padrao,
    criar_veiculo_padrao,
)


def _montar_use_case(cliente_repo=None, veiculo_repo=None, servico_repo=None, peca_repo=None):
    return CriarOrdemServicoUseCase(
        ordem_servico_repository=FakeOrdemServicoRepository(),
        cliente_repository=cliente_repo or FakeClienteRepository(),
        veiculo_repository=veiculo_repo or FakeVeiculoRepository(),
        servico_repository=servico_repo or FakeServicoRepository(),
        peca_repository=peca_repo or FakePecaRepository(),
    )


async def test_criar_ordem_servico_com_item_de_servico_e_peca():
    cliente_repo = FakeClienteRepository()
    veiculo_repo = FakeVeiculoRepository()
    servico_repo = FakeServicoRepository()
    peca_repo = FakePecaRepository()
    cliente = await criar_cliente_padrao(cliente_repo)
    veiculo = await criar_veiculo_padrao(veiculo_repo, cliente.id)
    servico = await criar_servico_padrao(servico_repo)
    peca = await criar_peca_padrao(peca_repo, quantidade=10)
    use_case = _montar_use_case(cliente_repo, veiculo_repo, servico_repo, peca_repo)

    resultado = await use_case.executar(
        CriarOrdemServicoInput(
            cliente_id=cliente.id,
            veiculo_id=veiculo.id,
            itens_servico=[ItemServicoInput(servico_id=servico.id)],
            itens_peca=[ItemPecaInput(peca_id=peca.id, quantidade=2)],
        )
    )

    assert resultado.id == 1
    assert resultado.orcamento.total_servicos == servico.preco.valor
    assert len(resultado.itens_peca) == 1
    peca_atualizada = await peca_repo.buscar_por_id(peca.id)
    assert peca_atualizada.quantidade_disponivel == 8


async def test_criar_ordem_servico_com_cliente_inexistente_levanta_erro():
    use_case = _montar_use_case()

    with pytest.raises(ClienteNaoEncontradoError):
        await use_case.executar(CriarOrdemServicoInput(cliente_id=999, veiculo_id=1))


async def test_criar_ordem_servico_com_veiculo_inexistente_levanta_erro():
    cliente_repo = FakeClienteRepository()
    cliente = await criar_cliente_padrao(cliente_repo)
    use_case = _montar_use_case(cliente_repo=cliente_repo)

    with pytest.raises(VeiculoNaoEncontradoError):
        await use_case.executar(CriarOrdemServicoInput(cliente_id=cliente.id, veiculo_id=999))


async def test_criar_ordem_servico_com_veiculo_de_outro_cliente_levanta_erro():
    cliente_repo = FakeClienteRepository()
    veiculo_repo = FakeVeiculoRepository()
    dono = await criar_cliente_padrao(cliente_repo)
    outro = await cliente_repo.criar(
        Cliente(
            nome="João", documento=Documento(valor="52998224725"), email="j@x.com", telefone="2"
        )
    )
    veiculo = await criar_veiculo_padrao(veiculo_repo, dono.id)
    use_case = _montar_use_case(cliente_repo=cliente_repo, veiculo_repo=veiculo_repo)

    with pytest.raises(VeiculoNaoPertenceAoClienteError):
        await use_case.executar(CriarOrdemServicoInput(cliente_id=outro.id, veiculo_id=veiculo.id))


async def test_criar_ordem_servico_com_servico_inexistente_levanta_erro():
    cliente_repo = FakeClienteRepository()
    veiculo_repo = FakeVeiculoRepository()
    cliente = await criar_cliente_padrao(cliente_repo)
    veiculo = await criar_veiculo_padrao(veiculo_repo, cliente.id)
    use_case = _montar_use_case(cliente_repo=cliente_repo, veiculo_repo=veiculo_repo)

    with pytest.raises(ServicoNaoEncontradoError):
        await use_case.executar(
            CriarOrdemServicoInput(
                cliente_id=cliente.id,
                veiculo_id=veiculo.id,
                itens_servico=[ItemServicoInput(servico_id=999)],
            )
        )


async def test_criar_ordem_servico_com_peca_inexistente_levanta_erro():
    cliente_repo = FakeClienteRepository()
    veiculo_repo = FakeVeiculoRepository()
    cliente = await criar_cliente_padrao(cliente_repo)
    veiculo = await criar_veiculo_padrao(veiculo_repo, cliente.id)
    use_case = _montar_use_case(cliente_repo=cliente_repo, veiculo_repo=veiculo_repo)

    with pytest.raises(PecaNaoEncontradaError):
        await use_case.executar(
            CriarOrdemServicoInput(
                cliente_id=cliente.id,
                veiculo_id=veiculo.id,
                itens_peca=[ItemPecaInput(peca_id=999, quantidade=1)],
            )
        )


async def test_criar_ordem_servico_com_estoque_insuficiente_levanta_erro():
    cliente_repo = FakeClienteRepository()
    veiculo_repo = FakeVeiculoRepository()
    peca_repo = FakePecaRepository()
    cliente = await criar_cliente_padrao(cliente_repo)
    veiculo = await criar_veiculo_padrao(veiculo_repo, cliente.id)
    peca = await criar_peca_padrao(peca_repo, quantidade=1)
    use_case = _montar_use_case(
        cliente_repo=cliente_repo, veiculo_repo=veiculo_repo, peca_repo=peca_repo
    )

    with pytest.raises(EstoqueInsuficienteError):
        await use_case.executar(
            CriarOrdemServicoInput(
                cliente_id=cliente.id,
                veiculo_id=veiculo.id,
                itens_peca=[ItemPecaInput(peca_id=peca.id, quantidade=5)],
            )
        )


async def test_criar_ordem_servico_sem_itens_levanta_erro():
    cliente_repo = FakeClienteRepository()
    veiculo_repo = FakeVeiculoRepository()
    cliente = await criar_cliente_padrao(cliente_repo)
    veiculo = await criar_veiculo_padrao(veiculo_repo, cliente.id)
    use_case = _montar_use_case(cliente_repo=cliente_repo, veiculo_repo=veiculo_repo)

    with pytest.raises(OrdemServicoSemItensError):
        await use_case.executar(
            CriarOrdemServicoInput(cliente_id=cliente.id, veiculo_id=veiculo.id)
        )
