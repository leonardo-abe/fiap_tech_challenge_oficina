from dataclasses import dataclass


@dataclass(frozen=True)
class AutenticarUsuarioInput:
    email: str
    senha: str
