from decimal import Decimal

from pydantic import BaseModel, Field


class PecaCreateSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descricao: str = Field(min_length=1, max_length=500)
    preco: Decimal = Field(gt=0)
    quantidade_inicial: int = Field(ge=0)


class PecaUpdateSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descricao: str = Field(min_length=1, max_length=500)
    preco: Decimal = Field(gt=0)


class ReporEstoqueSchema(BaseModel):
    quantidade: int = Field(gt=0)


class PecaSchema(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: Decimal
    quantidade_disponivel: int
