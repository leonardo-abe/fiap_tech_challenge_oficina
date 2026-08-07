import pytest

from app.domain.usuario.value_objects import Perfil


def test_perfil_e_string():
    assert Perfil.ADMIN == "ADMIN"


def test_perfil_a_partir_do_valor():
    assert Perfil("MECANICO") is Perfil.MECANICO


def test_perfil_valor_invalido_levanta_erro():
    with pytest.raises(ValueError):
        Perfil("GERENTE")
