from dataclasses import dataclass

from app.domain.usuario.value_objects import Perfil


@dataclass
class Usuario:
    nome: str
    email: str
    senha_hash: str
    perfil: Perfil
    id: int | None = None
    ativo: bool = True
