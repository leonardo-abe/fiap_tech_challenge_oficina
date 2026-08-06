from pydantic import BaseModel, EmailStr, Field


class ClienteCreateSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    documento: str = Field(min_length=11, max_length=18)
    email: EmailStr
    telefone: str = Field(min_length=8, max_length=20)


class ClienteUpdateSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    documento: str = Field(min_length=11, max_length=18)
    email: EmailStr
    telefone: str = Field(min_length=8, max_length=20)


class ClienteSchema(BaseModel):
    id: int
    nome: str
    documento: str
    email: EmailStr
    telefone: str
