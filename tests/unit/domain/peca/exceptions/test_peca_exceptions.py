from app.domain.peca.exceptions import (
    EstoqueInsuficienteError,
    PecaNaoEncontradaError,
    QuantidadeInvalidaError,
)
from app.domain.peca.exceptions.peca_error import PecaError


def test_peca_nao_encontrada_error_mensagem():
    erro = PecaNaoEncontradaError(42)

    assert "42" in str(erro)
    assert isinstance(erro, PecaError)


def test_estoque_insuficiente_error_mensagem():
    erro = EstoqueInsuficienteError(peca_id=1, disponivel=2, solicitado=5)

    mensagem = str(erro)
    assert "1" in mensagem
    assert "2" in mensagem
    assert "5" in mensagem


def test_quantidade_invalida_error_mensagem():
    erro = QuantidadeInvalidaError(-1)

    assert "-1" in str(erro)
