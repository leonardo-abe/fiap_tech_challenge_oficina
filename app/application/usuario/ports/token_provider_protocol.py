from typing import Protocol

from app.application.usuario.dtos import TokenPayload
from app.domain.usuario.value_objects import Perfil


class TokenProviderProtocol(Protocol):
    def gerar_token(self, usuario_id: int, perfil: Perfil) -> str: ...
    def decodificar_token(self, token: str) -> TokenPayload: ...
