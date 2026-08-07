from decimal import Decimal

from app.domain.cliente.entities import Cliente
from app.domain.cliente.value_objects import Documento
from app.domain.peca.entities import Peca
from app.domain.servico.entities import Servico
from app.domain.shared.value_objects import Money
from app.domain.veiculo.entities import Veiculo
from app.domain.veiculo.value_objects import Placa


async def criar_cliente_padrao(cliente_repository):
    return await cliente_repository.criar(
        Cliente(
            nome="Maria", documento=Documento(valor="11144477735"), email="m@x.com", telefone="1"
        )
    )


async def criar_veiculo_padrao(veiculo_repository, cliente_id):
    return await veiculo_repository.criar(
        Veiculo(
            cliente_id=cliente_id,
            placa=Placa(valor="ABC1234"),
            marca="Fiat",
            modelo="Uno",
            ano=2015,
        )
    )


async def criar_servico_padrao(servico_repository, preco=Decimal("80.00")):
    return await servico_repository.criar(
        Servico(nome="Troca de óleo", descricao="Óleo e filtro", preco=Money(valor=preco))
    )


async def criar_peca_padrao(peca_repository, quantidade=10, preco=Decimal("30.00")):
    return await peca_repository.criar(
        Peca(
            nome="Filtro",
            descricao="Filtro",
            preco=Money(valor=preco),
            quantidade_disponivel=quantidade,
        )
    )
