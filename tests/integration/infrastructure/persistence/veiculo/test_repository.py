from app.domain.cliente.entities import Cliente
from app.domain.cliente.value_objects import Documento
from app.domain.veiculo.entities import Veiculo
from app.domain.veiculo.value_objects import Placa
from app.infrastructure.persistence.cliente.repository import SQLAlchemyClienteRepository
from app.infrastructure.persistence.veiculo.repository import SQLAlchemyVeiculoRepository


async def _criar_cliente(session) -> int:
    cliente_repo = SQLAlchemyClienteRepository(session=session)
    cliente = await cliente_repo.criar(
        Cliente(
            nome="Maria", documento=Documento(valor="11144477735"), email="m@x.com", telefone="1"
        )
    )
    return cliente.id


def _veiculo(cliente_id: int, placa="ABC1234") -> Veiculo:
    return Veiculo(
        cliente_id=cliente_id, placa=Placa(valor=placa), marca="Fiat", modelo="Uno", ano=2015
    )


async def test_criar_e_buscar_por_id(session):
    cliente_id = await _criar_cliente(session)
    repositorio = SQLAlchemyVeiculoRepository(session=session)

    criado = await repositorio.criar(_veiculo(cliente_id))

    assert criado.id is not None
    encontrado = await repositorio.buscar_por_id(criado.id)
    assert encontrado.placa.valor == "ABC1234"


async def test_buscar_por_id_inexistente_retorna_none(session):
    repositorio = SQLAlchemyVeiculoRepository(session=session)

    assert await repositorio.buscar_por_id(999) is None


async def test_existe_com_placa(session):
    cliente_id = await _criar_cliente(session)
    repositorio = SQLAlchemyVeiculoRepository(session=session)
    await repositorio.criar(_veiculo(cliente_id))

    assert await repositorio.existe_com_placa("ABC1234") is True
    assert await repositorio.existe_com_placa("DEF5678") is False


async def test_listar_filtra_por_cliente(session):
    cliente_1 = await _criar_cliente(session)
    cliente_repo = SQLAlchemyClienteRepository(session=session)
    cliente_2 = await cliente_repo.criar(
        Cliente(
            nome="João", documento=Documento(valor="52998224725"), email="j@x.com", telefone="2"
        )
    )
    repositorio = SQLAlchemyVeiculoRepository(session=session)
    await repositorio.criar(_veiculo(cliente_1, placa="ABC1234"))
    await repositorio.criar(_veiculo(cliente_2.id, placa="DEF5678"))

    todos = await repositorio.listar()
    do_cliente_1 = await repositorio.listar(cliente_id=cliente_1)

    assert len(todos) == 2
    assert len(do_cliente_1) == 1
    assert do_cliente_1[0].placa.valor == "ABC1234"


async def test_atualizar_persiste_mudancas(session):
    cliente_id = await _criar_cliente(session)
    repositorio = SQLAlchemyVeiculoRepository(session=session)
    criado = await repositorio.criar(_veiculo(cliente_id))
    criado.placa = Placa(valor="DEF5678")
    criado.ano = 2020

    atualizado = await repositorio.atualizar(criado)

    assert atualizado.placa.valor == "DEF5678"
    assert atualizado.ano == 2020


async def test_remover_exclui_o_registro(session):
    cliente_id = await _criar_cliente(session)
    repositorio = SQLAlchemyVeiculoRepository(session=session)
    criado = await repositorio.criar(_veiculo(cliente_id))

    await repositorio.remover(criado.id)

    assert await repositorio.buscar_por_id(criado.id) is None
