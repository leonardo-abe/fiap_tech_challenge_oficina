import asyncio
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.peca.entities import Peca
from app.domain.peca.exceptions import EstoqueInsuficienteError, PecaNaoEncontradaError
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


async def test_atualizar_persiste_mudancas_mas_nao_toca_o_estoque(session):
    repositorio = SQLAlchemyPecaRepository(session=session)
    criada = await repositorio.criar(
        Peca(
            nome="Filtro",
            descricao="Filtro",
            preco=Money(valor=Decimal("30")),
            quantidade_disponivel=5,
        )
    )
    criada.nome = "Filtro premium"
    criada.preco = Money(valor=Decimal("35"))
    # mesmo setando isso na entidade em memória, atualizar() não deve persistir -
    # estoque só se move por decrementar_estoque/incrementar_estoque.
    criada.quantidade_disponivel = 999

    atualizada = await repositorio.atualizar(criada)

    assert atualizada.nome == "Filtro premium"
    assert atualizada.preco.valor == Decimal("35.00")
    assert atualizada.quantidade_disponivel == 5


def _peca(quantidade_disponivel: int) -> Peca:
    return Peca(
        nome="Filtro",
        descricao="Filtro",
        preco=Money(valor=Decimal("30")),
        quantidade_disponivel=quantidade_disponivel,
    )


async def test_decrementar_estoque_sucesso(session):
    repositorio = SQLAlchemyPecaRepository(session=session)
    criada = await repositorio.criar(_peca(10))

    atualizada = await repositorio.decrementar_estoque(criada.id, 4)

    assert atualizada.quantidade_disponivel == 6


async def test_decrementar_estoque_insuficiente_levanta_erro(session):
    repositorio = SQLAlchemyPecaRepository(session=session)
    criada = await repositorio.criar(_peca(3))

    with pytest.raises(EstoqueInsuficienteError):
        await repositorio.decrementar_estoque(criada.id, 5)

    # a tentativa que falhou não deve ter alterado o estoque
    inalterada = await repositorio.buscar_por_id(criada.id)
    assert inalterada.quantidade_disponivel == 3


async def test_decrementar_estoque_peca_inexistente_levanta_erro(session):
    repositorio = SQLAlchemyPecaRepository(session=session)

    with pytest.raises(PecaNaoEncontradaError):
        await repositorio.decrementar_estoque(999, 1)


async def test_incrementar_estoque_sucesso(session):
    repositorio = SQLAlchemyPecaRepository(session=session)
    criada = await repositorio.criar(_peca(5))

    atualizada = await repositorio.incrementar_estoque(criada.id, 7)

    assert atualizada.quantidade_disponivel == 12


async def test_incrementar_estoque_peca_inexistente_levanta_erro(session):
    repositorio = SQLAlchemyPecaRepository(session=session)

    with pytest.raises(PecaNaoEncontradaError):
        await repositorio.incrementar_estoque(999, 1)


async def test_decrementar_estoque_concorrente_nao_sofre_lost_update(engine):
    # prova o fim da race condition: duas transações decrementando a mesma peça ao
    # mesmo tempo, pedindo juntas mais do que o estoque disponível (8 + 5 = 13 > 10).
    # com o load-mutate-save antigo, as duas liam o mesmo valor e a que confirmasse
    # por último sobrescrevia a outra - nenhuma erro de estoque insuficiente era
    # disparado, mesmo faltando estoque para atender as duas. Com o UPDATE atômico
    # condicional, o lock de linha do Postgres serializa as duas transações: a
    # segunda a comitar reavalia a condição contra o valor já decrementado pela
    # primeira e falha corretamente.
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as setup_session:
        criada = await SQLAlchemyPecaRepository(session=setup_session).criar(
            Peca(
                nome="Pastilha de freio",
                descricao="Pastilha",
                preco=Money(valor=Decimal("50")),
                quantidade_disponivel=10,
            )
        )
        await setup_session.commit()
        peca_id = criada.id

    async def _decrementar(quantidade: int) -> tuple[int, str]:
        async with session_factory() as session:
            try:
                await SQLAlchemyPecaRepository(session=session).decrementar_estoque(
                    peca_id, quantidade
                )
                await session.commit()
                return quantidade, "ok"
            except EstoqueInsuficienteError:
                await session.rollback()
                return quantidade, "insuficiente"

    resultados = await asyncio.gather(_decrementar(8), _decrementar(5))

    situacoes = {situacao for _, situacao in resultados}
    assert situacoes == {"ok", "insuficiente"}

    quantidade_aplicada = next(qtd for qtd, situacao in resultados if situacao == "ok")
    async with session_factory() as session:
        final = await SQLAlchemyPecaRepository(session=session).buscar_por_id(peca_id)
        assert final.quantidade_disponivel == 10 - quantidade_aplicada


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
