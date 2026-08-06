from dataclasses import dataclass

from app.domain.usuario.value_objects import Perfil


@dataclass(frozen=True)
class UsuarioOutput:
    id: int
    nome: str
    email: str
    perfil: Perfil
    ativo: bool
