from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ItemServicoCreateSchema(BaseModel):
    servico_id: int


class ItemPecaCreateSchema(BaseModel):
    peca_id: int
    quantidade: int = Field(gt=0)


class OrdemServicoCreateSchema(BaseModel):
    cliente_id: int
    veiculo_id: int
    itens_servico: list[ItemServicoCreateSchema] = Field(default_factory=list)
    itens_peca: list[ItemPecaCreateSchema] = Field(default_factory=list)


class ItemServicoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    servico_id: int
    nome: str
    valor: Decimal


class ItemPecaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    peca_id: int
    nome: str
    quantidade: int
    valor_unitario: Decimal
    valor_total: Decimal


class OrcamentoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_servicos: Decimal
    total_pecas: Decimal
    total: Decimal


class OrdemServicoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    veiculo_id: int
    status: str
    recebida_em: datetime
    orcamento: OrcamentoSchema
    itens_servico: list[ItemServicoSchema]
    itens_peca: list[ItemPecaSchema]


class OrdemServicoStatusSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    recebida_em: datetime
    execucao_iniciada_em: datetime | None
    finalizada_em: datetime | None
