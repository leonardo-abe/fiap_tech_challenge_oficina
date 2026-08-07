from decimal import Decimal

from app.domain.cliente.entities import Cliente
from app.domain.cliente.value_objects import Documento
from app.domain.ordem_servico.entities import ItemPeca, ItemServico, OrdemServico
from app.domain.ordem_servico.value_objects import StatusOS
from app.domain.peca.entities import Peca
from app.domain.servico.entities import Servico
from app.domain.shared.value_objects import Money
from app.domain.veiculo.entities import Veiculo
from app.domain.veiculo.value_objects import Placa
from app.infrastructure.persistence.cliente.repository import SQLAlchemyClienteRepository
from app.infrastructure.persistence.ordem_servico.repository import (
    SQLAlchemyOrdemServicoRepository,
)
from app.infrastructure.persistence.peca.repository import SQLAlchemyPecaRepository
from app.infrastructure.persistence.servico.repository import SQLAlchemyServicoRepository
from app.infrastructure.persistence.veiculo.repository import SQLAlchemyVeiculoRepository


async def _preparar_cliente_e_veiculo(session) -> tuple[int, int]:
    cliente = await SQLAlchemyClienteRepository(session=session).criar(
        Cliente(
            nome="Maria", documento=Documento(valor="11144477735"), email="m@x.com", telefone="1"
        )
    )
    veiculo = await SQLAlchemyVeiculoRepository(session=session).criar(
        Veiculo(
            cliente_id=cliente.id,
            placa=Placa(valor="ABC1234"),
            marca="Fiat",
            modelo="Uno",
            ano=2015,
        )
    )
    return cliente.id, veiculo.id


async def _ordem_com_itens(session, cliente_id: int, veiculo_id: int) -> OrdemServico:
    servico = await SQLAlchemyServicoRepository(session=session).criar(
        Servico(nome="Troca de óleo", descricao="Óleo", preco=Money(valor=Decimal("80.00")))
    )
    peca = await SQLAlchemyPecaRepository(session=session).criar(
        Peca(
            nome="Filtro",
            descricao="Filtro",
            preco=Money(valor=Decimal("30.00")),
            quantidade_disponivel=10,
        )
    )

    ordem = OrdemServico(cliente_id=cliente_id, veiculo_id=veiculo_id)
    ordem.adicionar_item_servico(
        ItemServico(servico_id=servico.id, nome=servico.nome, valor=servico.preco)
    )
    ordem.adicionar_item_peca(
        ItemPeca(peca_id=peca.id, nome=peca.nome, quantidade=2, valor_unitario=peca.preco)
    )
    return ordem


async def test_criar_e_buscar_por_id_traz_itens(session):
    cliente_id, veiculo_id = await _preparar_cliente_e_veiculo(session)
    repositorio = SQLAlchemyOrdemServicoRepository(session=session)

    criada = await repositorio.criar(await _ordem_com_itens(session, cliente_id, veiculo_id))

    assert criada.id is not None
    assert len(criada.itens_servico) == 1
    assert len(criada.itens_peca) == 1

    encontrada = await repositorio.buscar_por_id(criada.id)
    assert encontrada.status == StatusOS.RECEBIDA
    assert encontrada.itens_servico[0].nome == "Troca de óleo"
    assert encontrada.itens_peca[0].valor_total.valor == Decimal("60.00")


async def test_buscar_por_id_inexistente_retorna_none(session):
    repositorio = SQLAlchemyOrdemServicoRepository(session=session)

    assert await repositorio.buscar_por_id(999) is None


async def test_listar_traz_todas_com_itens(session):
    cliente_id, veiculo_id = await _preparar_cliente_e_veiculo(session)
    repositorio = SQLAlchemyOrdemServicoRepository(session=session)
    await repositorio.criar(await _ordem_com_itens(session, cliente_id, veiculo_id))
    await repositorio.criar(OrdemServico(cliente_id=cliente_id, veiculo_id=veiculo_id))

    resultado = await repositorio.listar()

    assert len(resultado) == 2


async def test_atualizar_persiste_transicao_de_status(session):
    cliente_id, veiculo_id = await _preparar_cliente_e_veiculo(session)
    repositorio = SQLAlchemyOrdemServicoRepository(session=session)
    criada = await repositorio.criar(await _ordem_com_itens(session, cliente_id, veiculo_id))

    criada.mudar_status(StatusOS.EM_DIAGNOSTICO)
    atualizada = await repositorio.atualizar(criada)

    assert atualizada.status == StatusOS.EM_DIAGNOSTICO
    reconsultada = await repositorio.buscar_por_id(criada.id)
    assert reconsultada.status == StatusOS.EM_DIAGNOSTICO
