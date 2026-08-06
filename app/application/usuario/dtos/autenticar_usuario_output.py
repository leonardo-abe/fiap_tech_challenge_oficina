from dataclasses import dataclass, field


@dataclass(frozen=True)
class AutenticarUsuarioOutput:
    access_token: str
    token_type: str = field(default="bearer")
