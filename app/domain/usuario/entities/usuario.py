from dataclasses import dataclass, field

from app.domain.usuario.value_objects import Perfil


@dataclass
class Usuario:
    nome: str
    email: str
    senha_hash: str = field(repr=False)  # nunca deve aparecer em log/stack trace
    perfil: Perfil
    id: int | None = None
    ativo: bool = True
