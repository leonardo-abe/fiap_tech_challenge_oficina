from app.domain.cliente.entities import Cliente
from app.domain.cliente.value_objects import Documento
from app.infrastructure.persistence.cliente.repository import SQLAlchemyClienteRepository


def _cliente(documento="11144477735") -> Cliente:
    return Cliente(
        nome="Maria Silva", documento=Documento(valor=documento), email="maria@x.com", telefone="1"
    )


async def test_criar_e_buscar_por_id(session):
    repositorio = SQLAlchemyClienteRepository(session=session)

    criado = await repositorio.criar(_cliente())

    assert criado.id is not None
    encontrado = await repositorio.buscar_por_id(criado.id)
    assert encontrado.nome == "Maria Silva"
    assert encontrado.documento.valor == "11144477735"


async def test_buscar_por_id_inexistente_retorna_none(session):
    repositorio = SQLAlchemyClienteRepository(session=session)

    assert await repositorio.buscar_por_id(999) is None


async def test_existe_com_documento(session):
    repositorio = SQLAlchemyClienteRepository(session=session)
    await repositorio.criar(_cliente())

    assert await repositorio.existe_com_documento("11144477735") is True
    assert await repositorio.existe_com_documento("52998224725") is False


async def test_listar_ordenado_por_nome(session):
    repositorio = SQLAlchemyClienteRepository(session=session)
    await repositorio.criar(_cliente(documento="11144477735"))
    joao = Cliente(
        nome="Ana", documento=Documento(valor="52998224725"), email="ana@x.com", telefone="2"
    )
    await repositorio.criar(joao)

    resultado = await repositorio.listar()

    assert [cliente.nome for cliente in resultado] == ["Ana", "Maria Silva"]


async def test_atualizar_persiste_mudancas(session):
    repositorio = SQLAlchemyClienteRepository(session=session)
    criado = await repositorio.criar(_cliente())
    criado.nome = "Maria Souza"
    criado.email = "nova@x.com"

    atualizado = await repositorio.atualizar(criado)

    assert atualizado.nome == "Maria Souza"
    assert atualizado.email == "nova@x.com"


async def test_remover_exclui_o_registro(session):
    repositorio = SQLAlchemyClienteRepository(session=session)
    criado = await repositorio.criar(_cliente())

    await repositorio.remover(criado.id)

    assert await repositorio.buscar_por_id(criado.id) is None
