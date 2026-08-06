from dataclasses import dataclass

from app.domain.usuario.value_objects import Perfil


@dataclass(frozen=True)
class TokenPayload:
    usuario_id: int
    perfil: Perfil
