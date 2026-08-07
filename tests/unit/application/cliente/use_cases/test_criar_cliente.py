import pytest

from app.application.cliente.dtos import CriarClienteInput
from app.application.cliente.use_cases import CriarClienteUseCase
from app.domain.cliente.exceptions import DocumentoInvalidoError, DocumentoJaCadastradoError
from tests.unit.application.fakes import FakeClienteRepository


async def test_criar_cliente_sucesso():
    use_case = CriarClienteUseCase(FakeClienteRepository())

    resultado = await use_case.executar(
        CriarClienteInput(
            nome="Maria Silva",
            documento="11144477735",
            email="maria@example.com",
            telefone="11999998888",
        )
    )

    assert resultado.id == 1
    assert resultado.documento == "11144477735"


async def test_criar_cliente_com_documento_invalido_levanta_erro():
    use_case = CriarClienteUseCase(FakeClienteRepository())

    with pytest.raises(DocumentoInvalidoError):
        await use_case.executar(
            CriarClienteInput(
                nome="Maria Silva", documento="123", email="maria@example.com", telefone="119999"
            )
        )


async def test_criar_cliente_com_documento_ja_cadastrado_levanta_erro():
    repositorio = FakeClienteRepository()
    use_case = CriarClienteUseCase(repositorio)
    entrada = CriarClienteInput(
        nome="Maria Silva", documento="11144477735", email="maria@example.com", telefone="119999"
    )
    await use_case.executar(entrada)

    with pytest.raises(DocumentoJaCadastradoError):
        await use_case.executar(entrada)
