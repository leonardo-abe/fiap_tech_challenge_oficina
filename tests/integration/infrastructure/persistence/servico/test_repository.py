from decimal import Decimal

from app.domain.servico.entities import Servico
from app.domain.shared.value_objects import Money
from app.infrastructure.persistence.servico.repository import SQLAlchemyServicoRepository


def _servico(nome="Troca de óleo", preco=Decimal("120.00")) -> Servico:
    return Servico(nome=nome, descricao="Óleo e filtro", preco=Money(valor=preco))


async def test_criar_e_buscar_por_id(session):
    repositorio = SQLAlchemyServicoRepository(session=session)

    criado = await repositorio.criar(_servico())

    assert criado.id is not None
    encontrado = await repositorio.buscar_por_id(criado.id)
    assert encontrado.nome == "Troca de óleo"
    assert encontrado.preco.valor == Decimal("120.00")


async def test_buscar_por_id_inexistente_retorna_none(session):
    repositorio = SQLAlchemyServicoRepository(session=session)

    assert await repositorio.buscar_por_id(999) is None


async def test_listar_ordenado_por_nome(session):
    repositorio = SQLAlchemyServicoRepository(session=session)
    await repositorio.criar(_servico(nome="Troca de óleo"))
    await repositorio.criar(_servico(nome="Alinhamento"))

    resultado = await repositorio.listar()

    assert [servico.nome for servico in resultado] == ["Alinhamento", "Troca de óleo"]


async def test_atualizar_persiste_mudancas(session):
    repositorio = SQLAlchemyServicoRepository(session=session)
    criado = await repositorio.criar(_servico())
    criado.preco = Money(valor=Decimal("150.00"))

    atualizado = await repositorio.atualizar(criado)

    assert atualizado.preco.valor == Decimal("150.00")


async def test_remover_exclui_o_registro(session):
    repositorio = SQLAlchemyServicoRepository(session=session)
    criado = await repositorio.criar(_servico())

    await repositorio.remover(criado.id)

    assert await repositorio.buscar_por_id(criado.id) is None
