from pydantic import BaseModel, EmailStr, Field


class LoginRequestSchema(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1)


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"  # noqa: S105 - tipo de token OAuth2, não é uma senha
