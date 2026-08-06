from app.domain.veiculo.exceptions.placa_invalida import PlacaInvalidaError
from app.domain.veiculo.exceptions.placa_ja_cadastrada import PlacaJaCadastradaError
from app.domain.veiculo.exceptions.veiculo_error import VeiculoError
from app.domain.veiculo.exceptions.veiculo_nao_encontrado import VeiculoNaoEncontradoError

__all__ = [
    "PlacaInvalidaError",
    "PlacaJaCadastradaError",
    "VeiculoError",
    "VeiculoNaoEncontradoError",
]
