from app.application.usuario.dtos import CriarUsuarioInput, UsuarioOutput
from app.application.usuario.ports import PasswordHasherProtocol, UsuarioRepositoryProtocol
from app.domain.usuario.entities import Usuario
from app.domain.usuario.exceptions import EmailJaCadastradoError


class CriarUsuarioUseCase:
    def __init__(
        self,
        usuario_repository: UsuarioRepositoryProtocol,
        password_hasher: PasswordHasherProtocol,
    ) -> None:
        self._usuario_repository = usuario_repository
        self._password_hasher = password_hasher

    async def executar(self, entrada: CriarUsuarioInput) -> UsuarioOutput:
        if await self._usuario_repository.existe_com_email(entrada.email):
            raise EmailJaCadastradoError

        usuario = Usuario(
            nome=entrada.nome,
            email=entrada.email,
            senha_hash=self._password_hasher.hash(entrada.senha),
            perfil=entrada.perfil,
        )
        usuario_criado = await self._usuario_repository.criar(usuario)

        return UsuarioOutput(
            id=usuario_criado.id,
            nome=usuario_criado.nome,
            email=usuario_criado.email,
            perfil=usuario_criado.perfil,
            ativo=usuario_criado.ativo,
        )
