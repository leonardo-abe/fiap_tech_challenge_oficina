from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.ordem_servico.value_objects import StatusOS
from app.infrastructure.db.session import Base
from app.infrastructure.persistence.ordem_servico.models.item_peca_model import ItemPecaModel
from app.infrastructure.persistence.ordem_servico.models.item_servico_model import (
    ItemServicoModel,
)


class OrdemServicoModel(Base):
    __tablename__ = "ordens_servico"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False, index=True)
    veiculo_id: Mapped[int] = mapped_column(ForeignKey("veiculos.id"), nullable=False, index=True)
    status: Mapped[StatusOS] = mapped_column(Enum(StatusOS, name="status_os"), nullable=False)
    recebida_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    execucao_iniciada_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    finalizada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    itens_servico: Mapped[list[ItemServicoModel]] = relationship(
        back_populates="ordem_servico", cascade="all, delete-orphan"
    )
    itens_peca: Mapped[list[ItemPecaModel]] = relationship(
        back_populates="ordem_servico", cascade="all, delete-orphan"
    )
