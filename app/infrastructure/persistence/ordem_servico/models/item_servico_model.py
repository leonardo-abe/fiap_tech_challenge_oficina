from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base


class ItemServicoModel(Base):
    __tablename__ = "itens_servico"

    id: Mapped[int] = mapped_column(primary_key=True)
    ordem_servico_id: Mapped[int] = mapped_column(
        ForeignKey("ordens_servico.id"), nullable=False, index=True
    )
    servico_id: Mapped[int] = mapped_column(ForeignKey("servicos.id"), nullable=False)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    valor: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)

    ordem_servico: Mapped["OrdemServicoModel"] = relationship(  # noqa: F821
        back_populates="itens_servico"
    )
