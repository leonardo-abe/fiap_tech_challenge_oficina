import pytest

from app.domain.usuario.exceptions import (
    CredenciaisInvalidasError,
    EmailJaCadastradoError,
    TokenInvalidoError,
    UsuarioError,
)


@pytest.mark.parametrize(
    "excecao", [CredenciaisInvalidasError, EmailJaCadastradoError, TokenInvalidoError]
)
def test_excecoes_de_usuario_sao_subclasses_de_usuario_error(excecao):
    with pytest.raises(UsuarioError):
        raise excecao
