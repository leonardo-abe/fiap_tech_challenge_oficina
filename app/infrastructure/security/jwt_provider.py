from datetime import UTC, datetime, timedelta

import jwt

from app.application.usuario.dtos import TokenPayload
from app.domain.usuario.exceptions import TokenInvalidoError
from app.domain.usuario.value_objects import Perfil
from app.shared.settings import settings


class JWTTokenProvider:
    _ALGORITHM = "HS256"

    def gerar_token(self, usuario_id: int, perfil: Perfil) -> str:
        agora = datetime.now(UTC)
        payload = {
            "sub": str(usuario_id),
            "perfil": perfil.value,
            "iat": agora,
            "exp": agora + timedelta(minutes=settings.jwt_expiracao_minutos),
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=self._ALGORITHM)

    def decodificar_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[self._ALGORITHM])
        except jwt.PyJWTError as erro:
            raise TokenInvalidoError from erro

        return TokenPayload(usuario_id=int(payload["sub"]), perfil=Perfil(payload["perfil"]))
