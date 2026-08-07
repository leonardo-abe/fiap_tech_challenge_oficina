import pytest

from app.application.veiculo.dtos import CriarVeiculoInput
from app.application.veiculo.use_cases import BuscarVeiculoUseCase, CriarVeiculoUseCase
from app.domain.cliente.entities import Cliente
from app.domain.cliente.value_objects import Documento
from app.domain.veiculo.exceptions import VeiculoNaoEncontradoError
from tests.unit.application.fakes import FakeClienteRepository, FakeVeiculoRepository


async def test_buscar_veiculo_existente():
    cliente_repository = FakeClienteRepository()
    cliente = await cliente_repository.criar(
        Cliente(
            nome="Maria", documento=Documento(valor="11144477735"), email="m@x.com", telefone="1"
        )
    )
    veiculo_repository = FakeVeiculoRepository()
    criado = await CriarVeiculoUseCase(veiculo_repository, cliente_repository).executar(
        CriarVeiculoInput(
            cliente_id=cliente.id, placa="ABC1234", marca="Fiat", modelo="Uno", ano=2015
        )
    )

    resultado = await BuscarVeiculoUseCase(veiculo_repository).executar(criado.id)

    assert resultado.placa == "ABC1234"


async def test_buscar_veiculo_inexistente_levanta_erro():
    use_case = BuscarVeiculoUseCase(FakeVeiculoRepository())

    with pytest.raises(VeiculoNaoEncontradoError):
        await use_case.executar(999)
