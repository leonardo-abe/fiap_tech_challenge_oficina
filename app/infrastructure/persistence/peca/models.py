from sqlalchemy import CheckConstraint, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.session import Base


class PecaModel(Base):
    __tablename__ = "pecas"
    __table_args__ = (
        CheckConstraint("quantidade_disponivel >= 0", name="ck_pecas_quantidade_nao_negativa"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(500), nullable=False)
    preco: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    quantidade_disponivel: Mapped[int] = mapped_column(Integer, nullable=False)
