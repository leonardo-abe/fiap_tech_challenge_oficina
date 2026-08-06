from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.usuario.entities import Usuario
from app.infrastructure.persistence.usuario.models import UsuarioModel


class SQLAlchemyUsuarioRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def buscar_por_email(self, email: str) -> Usuario | None:
        resultado = await self._session.execute(
            select(UsuarioModel).where(UsuarioModel.email == email)
        )
        model = resultado.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        model = await self._session.get(UsuarioModel, usuario_id)
        return self._to_entity(model) if model else None

    async def existe_com_email(self, email: str) -> bool:
        resultado = await self._session.execute(
            select(UsuarioModel.id).where(UsuarioModel.email == email)
        )
        return resultado.scalar_one_or_none() is not None

    async def criar(self, usuario: Usuario) -> Usuario:
        model = UsuarioModel(
            nome=usuario.nome,
            email=usuario.email,
            senha_hash=usuario.senha_hash,
            perfil=usuario.perfil,
            ativo=usuario.ativo,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: UsuarioModel) -> Usuario:
        return Usuario(
            id=model.id,
            nome=model.nome,
            email=model.email,
            senha_hash=model.senha_hash,
            perfil=model.perfil,
            ativo=model.ativo,
        )
