import pytest

from app.application.veiculo.dtos import CriarVeiculoInput
from app.application.veiculo.use_cases import BuscarVeiculoPorPlacaUseCase, CriarVeiculoUseCase
from app.domain.cliente.entities import Cliente
from app.domain.cliente.value_objects import Documento
from app.domain.veiculo.exceptions import PlacaInvalidaError, VeiculoNaoEncontradoError
from tests.unit.application.fakes import FakeClienteRepository, FakeVeiculoRepository


async def test_buscar_veiculo_por_placa_encontrado():
    cliente_repository = FakeClienteRepository()
    cliente = await cliente_repository.criar(
        Cliente(
            nome="Maria", documento=Documento(valor="11144477735"), email="m@x.com", telefone="1"
        )
    )
    veiculo_repository = FakeVeiculoRepository()
    await CriarVeiculoUseCase(veiculo_repository, cliente_repository).executar(
        CriarVeiculoInput(
            cliente_id=cliente.id, placa="ABC1234", marca="Fiat", modelo="Uno", ano=2015
        )
    )

    resultado = await BuscarVeiculoPorPlacaUseCase(veiculo_repository).executar("ABC1234")

    assert resultado.marca == "Fiat"
    assert resultado.placa == "ABC1234"


async def test_buscar_veiculo_por_placa_nao_encontrada_levanta_erro():
    with pytest.raises(VeiculoNaoEncontradoError):
        await BuscarVeiculoPorPlacaUseCase(FakeVeiculoRepository()).executar("XYZ9999")


async def test_buscar_veiculo_por_placa_invalida_levanta_erro():
    with pytest.raises(PlacaInvalidaError):
        await BuscarVeiculoPorPlacaUseCase(FakeVeiculoRepository()).executar("123")
