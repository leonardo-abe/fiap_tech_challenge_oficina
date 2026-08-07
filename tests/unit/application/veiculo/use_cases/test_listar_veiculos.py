from app.application.veiculo.dtos import CriarVeiculoInput
from app.application.veiculo.use_cases import CriarVeiculoUseCase, ListarVeiculosUseCase
from app.domain.cliente.entities import Cliente
from app.domain.cliente.value_objects import Documento
from tests.unit.application.fakes import FakeClienteRepository, FakeVeiculoRepository


async def test_listar_veiculos_filtra_por_cliente():
    cliente_repository = FakeClienteRepository()
    cliente_1 = await cliente_repository.criar(
        Cliente(
            nome="Maria", documento=Documento(valor="11144477735"), email="m@x.com", telefone="1"
        )
    )
    cliente_2 = await cliente_repository.criar(
        Cliente(
            nome="João", documento=Documento(valor="52998224725"), email="j@x.com", telefone="2"
        )
    )
    veiculo_repository = FakeVeiculoRepository()
    criar_use_case = CriarVeiculoUseCase(veiculo_repository, cliente_repository)
    await criar_use_case.executar(
        CriarVeiculoInput(
            cliente_id=cliente_1.id, placa="ABC1234", marca="Fiat", modelo="Uno", ano=2015
        )
    )
    await criar_use_case.executar(
        CriarVeiculoInput(
            cliente_id=cliente_2.id, placa="DEF5678", marca="Ford", modelo="Ka", ano=2018
        )
    )

    todos = await ListarVeiculosUseCase(veiculo_repository).executar()
    do_cliente_1 = await ListarVeiculosUseCase(veiculo_repository).executar(cliente_id=cliente_1.id)

    assert len(todos) == 2
    assert len(do_cliente_1) == 1
    assert do_cliente_1[0].placa == "ABC1234"
