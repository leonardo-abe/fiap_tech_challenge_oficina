from app.domain.usuario.value_objects import Perfil
from app.infrastructure.security.jwt_provider import JWTTokenProvider

_token_provider = JWTTokenProvider()


def auth_headers(perfil: Perfil, usuario_id: int = 1) -> dict[str, str]:
    token = _token_provider.gerar_token(usuario_id=usuario_id, perfil=perfil)
    return {"Authorization": f"Bearer {token}"}
