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
