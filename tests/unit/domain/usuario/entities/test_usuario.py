from app.domain.usuario.entities import Usuario
from app.domain.usuario.value_objects import Perfil


def test_criar_usuario_com_valores_padrao():
    usuario = Usuario(
        nome="João Mecânico",
        email="joao@example.com",
        senha_hash="hash-opaco",
        perfil=Perfil.MECANICO,
        id=1,
    )

    assert usuario.perfil == Perfil.MECANICO
    assert usuario.ativo is True


def test_criar_usuario_inativo():
    usuario = Usuario(
        nome="João",
        email="joao@example.com",
        senha_hash="hash-opaco",
        perfil=Perfil.ADMIN,
        ativo=False,
    )

    assert usuario.ativo is False


def test_repr_do_usuario_nao_expoe_o_hash_da_senha():
    # ID-006: senha_hash não pode aparecer em log/stack trace via repr() acidental.
    usuario = Usuario(
        nome="João",
        email="joao@example.com",
        senha_hash="hash-secreto-que-nao-pode-aparecer",
        perfil=Perfil.MECANICO,
    )

    assert "hash-secreto-que-nao-pode-aparecer" not in repr(usuario)
