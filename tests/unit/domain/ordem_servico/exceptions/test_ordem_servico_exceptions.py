from app.domain.ordem_servico.exceptions import (
    OrdemServicoNaoEncontradaError,
    VeiculoNaoPertenceAoClienteError,
)
from app.domain.ordem_servico.exceptions.ordem_servico_error import OrdemServicoError


def test_ordem_servico_nao_encontrada_error_mensagem():
    erro = OrdemServicoNaoEncontradaError(7)

    assert "7" in str(erro)
    assert isinstance(erro, OrdemServicoError)


def test_veiculo_nao_pertence_ao_cliente_error_mensagem():
    erro = VeiculoNaoPertenceAoClienteError(veiculo_id=3, cliente_id=9)

    mensagem = str(erro)
    assert "3" in mensagem
    assert "9" in mensagem
