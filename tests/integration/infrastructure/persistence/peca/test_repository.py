from decimal import Decimal

from app.domain.peca.entities import Peca
from app.domain.shared.value_objects import Money
from app.infrastructure.persistence.peca.repository import SQLAlchemyPecaRepository


async def test_criar_e_buscar_por_id(session):
    repositorio = SQLAlchemyPecaRepository(session=session)
    peca = Peca(
        nome="Filtro de óleo",
        descricao="Filtro compatível com motores 1.0/1.6",
        preco=Money(valor=Decimal("39.90")),
        quantidade_disponivel=10,
    )

    criada = await repositorio.criar(peca)
    await session.commit()

    assert criada.id is not None
    encontrada = await repositorio.buscar_por_id(criada.id)
    assert encontrada is not None
    assert encontrada.nome == "Filtro de óleo"
    assert encontrada.preco.valor == Decimal("39.90")
    assert encontrada.quantidade_disponivel == 10


async def test_buscar_por_id_inexistente_retorna_none(session):
    repositorio = SQLAlchemyPecaRepository(session=session)

    assert await repositorio.buscar_por_id(999) is None


async def test_listar_retorna_todas_ordenadas_por_nome(session):
    repositorio = SQLAlchemyPecaRepository(session=session)
    await repositorio.criar(
        Peca(
            nome="Vela", descricao="Vela", preco=Money(valor=Decimal("10")), quantidade_disponivel=1
        )
    )
    await repositorio.criar(
        Peca(
            nome="Amortecedor",
            descricao="Amort.",
            preco=Money(valor=Decimal("200")),
            quantidade_disponivel=2,
        )
    )

    resultado = await repositorio.listar()

    assert [peca.nome for peca in resultado] == ["Amortecedor", "Vela"]


async def test_atualizar_persiste_mudancas(session):
    repositorio = SQLAlchemyPecaRepository(session=session)
    criada = await repositorio.criar(
        Peca(
            nome="Filtro",
            descricao="Filtro",
            preco=Money(valor=Decimal("30")),
            quantidade_disponivel=5,
        )
    )
    criada.quantidade_disponivel = 3
    criada.preco = Money(valor=Decimal("35"))

    atualizada = await repositorio.atualizar(criada)

    assert atualizada.quantidade_disponivel == 3
    assert atualizada.preco.valor == Decimal("35.00")


async def test_remover_exclui_o_registro(session):
    repositorio = SQLAlchemyPecaRepository(session=session)
    criada = await repositorio.criar(
        Peca(
            nome="Filtro",
            descricao="Filtro",
            preco=Money(valor=Decimal("30")),
            quantidade_disponivel=5,
        )
    )

    await repositorio.remover(criada.id)

    assert await repositorio.buscar_por_id(criada.id) is None
