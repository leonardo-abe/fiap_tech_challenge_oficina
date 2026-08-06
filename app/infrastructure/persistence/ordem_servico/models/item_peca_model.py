from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base


class ItemPecaModel(Base):
    __tablename__ = "itens_peca"

    id: Mapped[int] = mapped_column(primary_key=True)
    ordem_servico_id: Mapped[int] = mapped_column(
        ForeignKey("ordens_servico.id"), nullable=False, index=True
    )
    peca_id: Mapped[int] = mapped_column(ForeignKey("pecas.id"), nullable=False)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_unitario: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)

    ordem_servico: Mapped["OrdemServicoModel"] = relationship(  # noqa: F821
        back_populates="itens_peca"
    )
