import pytest

from app.application.veiculo.dtos import AtualizarVeiculoInput, CriarVeiculoInput
from app.application.veiculo.use_cases import AtualizarVeiculoUseCase, CriarVeiculoUseCase
from app.domain.cliente.entities import Cliente
from app.domain.cliente.exceptions import ClienteNaoEncontradoError
from app.domain.cliente.value_objects import Documento
from app.domain.veiculo.exceptions import PlacaJaCadastradaError, VeiculoNaoEncontradoError
from tests.unit.application.fakes import FakeClienteRepository, FakeVeiculoRepository


async def _preparar(cliente_repository, veiculo_repository):
    cliente = await cliente_repository.criar(
        Cliente(
            nome="Maria", documento=Documento(valor="11144477735"), email="m@x.com", telefone="1"
        )
    )
    criado = await CriarVeiculoUseCase(veiculo_repository, cliente_repository).executar(
        CriarVeiculoInput(
            cliente_id=cliente.id, placa="ABC1234", marca="Fiat", modelo="Uno", ano=2015
        )
    )
    return cliente, criado


async def test_atualizar_veiculo_sucesso():
    cliente_repository = FakeClienteRepository()
    veiculo_repository = FakeVeiculoRepository()
    cliente, criado = await _preparar(cliente_repository, veiculo_repository)

    resultado = await AtualizarVeiculoUseCase(veiculo_repository, cliente_repository).executar(
        criado.id,
        AtualizarVeiculoInput(
            cliente_id=cliente.id, placa="DEF5678", marca="Fiat", modelo="Uno", ano=2016
        ),
    )

    assert resultado.placa == "DEF5678"
    assert resultado.ano == 2016


async def test_atualizar_veiculo_inexistente_levanta_erro():
    use_case = AtualizarVeiculoUseCase(FakeVeiculoRepository(), FakeClienteRepository())

    with pytest.raises(VeiculoNaoEncontradoError):
        await use_case.executar(
            999,
            AtualizarVeiculoInput(
                cliente_id=1, placa="ABC1234", marca="Fiat", modelo="Uno", ano=2015
            ),
        )


async def test_atualizar_veiculo_com_cliente_inexistente_levanta_erro():
    cliente_repository = FakeClienteRepository()
    veiculo_repository = FakeVeiculoRepository()
    _, criado = await _preparar(cliente_repository, veiculo_repository)

    with pytest.raises(ClienteNaoEncontradoError):
        await AtualizarVeiculoUseCase(veiculo_repository, cliente_repository).executar(
            criado.id,
            AtualizarVeiculoInput(
                cliente_id=999, placa="ABC1234", marca="Fiat", modelo="Uno", ano=2015
            ),
        )


async def test_atualizar_veiculo_para_placa_ja_cadastrada_levanta_erro():
    cliente_repository = FakeClienteRepository()
    veiculo_repository = FakeVeiculoRepository()
    cliente, criado = await _preparar(cliente_repository, veiculo_repository)
    outro = await CriarVeiculoUseCase(veiculo_repository, cliente_repository).executar(
        CriarVeiculoInput(
            cliente_id=cliente.id, placa="DEF5678", marca="Ford", modelo="Ka", ano=2018
        )
    )

    with pytest.raises(PlacaJaCadastradaError):
        await AtualizarVeiculoUseCase(veiculo_repository, cliente_repository).executar(
            outro.id,
            AtualizarVeiculoInput(
                cliente_id=cliente.id, placa="ABC1234", marca="Ford", modelo="Ka", ano=2018
            ),
        )
