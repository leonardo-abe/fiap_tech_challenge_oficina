from pydantic import BaseModel, Field


class VeiculoCreateSchema(BaseModel):
    cliente_id: int
    placa: str = Field(min_length=7, max_length=8)
    marca: str = Field(min_length=1, max_length=50)
    modelo: str = Field(min_length=1, max_length=50)
    ano: int = Field(ge=1900, le=2100)


class VeiculoUpdateSchema(BaseModel):
    cliente_id: int
    placa: str = Field(min_length=7, max_length=8)
    marca: str = Field(min_length=1, max_length=50)
    modelo: str = Field(min_length=1, max_length=50)
    ano: int = Field(ge=1900, le=2100)


class VeiculoSchema(BaseModel):
    id: int
    cliente_id: int
    placa: str
    marca: str
    modelo: str
    ano: int
