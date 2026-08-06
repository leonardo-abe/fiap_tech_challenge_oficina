from dataclasses import dataclass

from app.domain.usuario.value_objects import Perfil


@dataclass(frozen=True)
class CriarUsuarioInput:
    nome: str
    email: str
    senha: str
    perfil: Perfil
