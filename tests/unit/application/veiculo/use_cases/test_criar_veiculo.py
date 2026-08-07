import pytest

from app.application.veiculo.dtos import CriarVeiculoInput
from app.application.veiculo.use_cases import CriarVeiculoUseCase
from app.domain.cliente.entities import Cliente
from app.domain.cliente.exceptions import ClienteNaoEncontradoError
from app.domain.cliente.value_objects import Documento
from app.domain.veiculo.exceptions import PlacaInvalidaError, PlacaJaCadastradaError
from tests.unit.application.fakes import FakeClienteRepository, FakeVeiculoRepository


async def _criar_cliente(cliente_repository: FakeClienteRepository) -> int:
    cliente = await cliente_repository.criar(
        Cliente(
            nome="Maria", documento=Documento(valor="11144477735"), email="m@x.com", telefone="1"
        )
    )
    return cliente.id


async def test_criar_veiculo_sucesso():
    cliente_repository = FakeClienteRepository()
    cliente_id = await _criar_cliente(cliente_repository)
    use_case = CriarVeiculoUseCase(FakeVeiculoRepository(), cliente_repository)

    resultado = await use_case.executar(
        CriarVeiculoInput(
            cliente_id=cliente_id, placa="ABC1234", marca="Fiat", modelo="Uno", ano=2015
        )
    )

    assert resultado.id == 1
    assert resultado.placa == "ABC1234"


async def test_criar_veiculo_com_cliente_inexistente_levanta_erro():
    use_case = CriarVeiculoUseCase(FakeVeiculoRepository(), FakeClienteRepository())

    with pytest.raises(ClienteNaoEncontradoError):
        await use_case.executar(
            CriarVeiculoInput(cliente_id=999, placa="ABC1234", marca="Fiat", modelo="Uno", ano=2015)
        )


async def test_criar_veiculo_com_placa_invalida_levanta_erro():
    cliente_repository = FakeClienteRepository()
    cliente_id = await _criar_cliente(cliente_repository)
    use_case = CriarVeiculoUseCase(FakeVeiculoRepository(), cliente_repository)

    with pytest.raises(PlacaInvalidaError):
        await use_case.executar(
            CriarVeiculoInput(
                cliente_id=cliente_id, placa="123", marca="Fiat", modelo="Uno", ano=2015
            )
        )


async def test_criar_veiculo_com_placa_ja_cadastrada_levanta_erro():
    cliente_repository = FakeClienteRepository()
    cliente_id = await _criar_cliente(cliente_repository)
    use_case = CriarVeiculoUseCase(FakeVeiculoRepository(), cliente_repository)
    entrada = CriarVeiculoInput(
        cliente_id=cliente_id, placa="ABC1234", marca="Fiat", modelo="Uno", ano=2015
    )
    await use_case.executar(entrada)

    with pytest.raises(PlacaJaCadastradaError):
        await use_case.executar(entrada)
