from app.domain.veiculo.exceptions import (
    PlacaInvalidaError,
    PlacaJaCadastradaError,
    VeiculoNaoEncontradoError,
)
from app.domain.veiculo.exceptions.veiculo_error import VeiculoError


def test_placa_invalida_error_mensagem():
    erro = PlacaInvalidaError("ABC123")

    assert "ABC123" in str(erro)
    assert isinstance(erro, VeiculoError)


def test_placa_ja_cadastrada_error_mensagem():
    erro = PlacaJaCadastradaError("ABC1234")

    assert "ABC1234" in str(erro)


def test_veiculo_nao_encontrado_error_mensagem():
    erro = VeiculoNaoEncontradoError(5)

    assert "5" in str(erro)
