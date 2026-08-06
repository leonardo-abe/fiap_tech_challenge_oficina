from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.session import Base


class ServicoModel(Base):
    __tablename__ = "servicos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(500), nullable=False)
    preco: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
