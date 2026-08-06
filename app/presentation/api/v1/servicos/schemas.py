from decimal import Decimal

from pydantic import BaseModel, Field


class ServicoCreateSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descricao: str = Field(min_length=1, max_length=500)
    preco: Decimal = Field(gt=0)


class ServicoUpdateSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descricao: str = Field(min_length=1, max_length=500)
    preco: Decimal = Field(gt=0)


class ServicoSchema(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: Decimal
