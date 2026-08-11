import pytest

from app.application.cliente.dtos import CriarClienteInput
from app.application.cliente.use_cases import BuscarClientePorDocumentoUseCase, CriarClienteUseCase
from app.domain.cliente.exceptions import ClienteNaoEncontradoError, DocumentoInvalidoError
from tests.unit.application.fakes import FakeClienteRepository


async def test_buscar_cliente_por_documento_encontrado():
    repositorio = FakeClienteRepository()
    await CriarClienteUseCase(repositorio).executar(
        CriarClienteInput(
            nome="Maria Silva", documento="11144477735", email="maria@x.com", telefone="1199999"
        )
    )

    resultado = await BuscarClientePorDocumentoUseCase(repositorio).executar("11144477735")

    assert resultado.nome == "Maria Silva"
    assert resultado.documento == "11144477735"


async def test_buscar_cliente_por_documento_nao_encontrado_levanta_erro():
    with pytest.raises(ClienteNaoEncontradoError):
        await BuscarClientePorDocumentoUseCase(FakeClienteRepository()).executar("52998224725")


async def test_buscar_cliente_por_documento_invalido_levanta_erro():
    with pytest.raises(DocumentoInvalidoError):
        await BuscarClientePorDocumentoUseCase(FakeClienteRepository()).executar("123")
