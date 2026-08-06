from pydantic import BaseModel, EmailStr, Field

from app.domain.usuario.value_objects import Perfil


class UsuarioCreateSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=8)
    perfil: Perfil


class UsuarioSchema(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: Perfil
    ativo: bool
