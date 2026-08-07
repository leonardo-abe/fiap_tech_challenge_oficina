import pytest

from app.application.veiculo.dtos import CriarVeiculoInput
from app.application.veiculo.use_cases import CriarVeiculoUseCase, RemoverVeiculoUseCase
from app.domain.cliente.entities import Cliente
from app.domain.cliente.value_objects import Documento
from app.domain.veiculo.exceptions import VeiculoNaoEncontradoError
from tests.unit.application.fakes import FakeClienteRepository, FakeVeiculoRepository


async def test_remover_veiculo_sucesso():
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

    await RemoverVeiculoUseCase(veiculo_repository).executar(criado.id)

    assert await veiculo_repository.buscar_por_id(criado.id) is None


async def test_remover_veiculo_inexistente_levanta_erro():
    use_case = RemoverVeiculoUseCase(FakeVeiculoRepository())

    with pytest.raises(VeiculoNaoEncontradoError):
        await use_case.executar(999)
