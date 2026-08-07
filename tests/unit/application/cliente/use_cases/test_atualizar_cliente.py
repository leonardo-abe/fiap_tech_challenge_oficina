import pytest

from app.application.cliente.dtos import AtualizarClienteInput, CriarClienteInput
from app.application.cliente.use_cases import AtualizarClienteUseCase, CriarClienteUseCase
from app.domain.cliente.exceptions import ClienteNaoEncontradoError, DocumentoJaCadastradoError
from tests.unit.application.fakes import FakeClienteRepository


async def test_atualizar_cliente_sucesso():
    repositorio = FakeClienteRepository()
    criado = await CriarClienteUseCase(repositorio).executar(
        CriarClienteInput(
            nome="Maria Silva", documento="11144477735", email="maria@x.com", telefone="1199999"
        )
    )

    resultado = await AtualizarClienteUseCase(repositorio).executar(
        criado.id,
        AtualizarClienteInput(
            nome="Maria Souza", documento="11144477735", email="nova@x.com", telefone="1188888"
        ),
    )

    assert resultado.nome == "Maria Souza"
    assert resultado.email == "nova@x.com"


async def test_atualizar_cliente_inexistente_levanta_erro():
    use_case = AtualizarClienteUseCase(FakeClienteRepository())

    with pytest.raises(ClienteNaoEncontradoError):
        await use_case.executar(
            999,
            AtualizarClienteInput(
                nome="Maria", documento="11144477735", email="m@x.com", telefone="1199999"
            ),
        )


async def test_atualizar_cliente_para_documento_ja_cadastrado_levanta_erro():
    repositorio = FakeClienteRepository()
    criar_use_case = CriarClienteUseCase(repositorio)
    await criar_use_case.executar(
        CriarClienteInput(
            nome="Maria", documento="11144477735", email="maria@x.com", telefone="1199999"
        )
    )
    joao = await criar_use_case.executar(
        CriarClienteInput(
            nome="João", documento="52998224725", email="joao@x.com", telefone="1188888"
        )
    )

    with pytest.raises(DocumentoJaCadastradoError):
        await AtualizarClienteUseCase(repositorio).executar(
            joao.id,
            AtualizarClienteInput(
                nome="João", documento="11144477735", email="joao@x.com", telefone="1188888"
            ),
        )


async def test_atualizar_cliente_mantendo_o_mesmo_documento_nao_levanta_erro():
    repositorio = FakeClienteRepository()
    criado = await CriarClienteUseCase(repositorio).executar(
        CriarClienteInput(
            nome="Maria", documento="11144477735", email="maria@x.com", telefone="1199999"
        )
    )

    resultado = await AtualizarClienteUseCase(repositorio).executar(
        criado.id,
        AtualizarClienteInput(
            nome="Maria Nova", documento="11144477735", email="maria@x.com", telefone="1199999"
        ),
    )

    assert resultado.nome == "Maria Nova"
