from app.application.usuario.dtos import AutenticarUsuarioInput, AutenticarUsuarioOutput
from app.application.usuario.ports import (
    PasswordHasherProtocol,
    TokenProviderProtocol,
    UsuarioRepositoryProtocol,
)
from app.domain.usuario.exceptions import CredenciaisInvalidasError


class AutenticarUsuarioUseCase:
    def __init__(
        self,
        usuario_repository: UsuarioRepositoryProtocol,
        password_hasher: PasswordHasherProtocol,
        token_provider: TokenProviderProtocol,
        hash_sem_correspondencia: str,
    ) -> None:
        self._usuario_repository = usuario_repository
        self._password_hasher = password_hasher
        self._token_provider = token_provider
        # Hash válido, mas sem correspondência possível: usado quando o e-mail não
        # existe, para que o custo de verificação seja o mesmo de uma senha errada e não
        # vaze, por tempo de resposta, se o e-mail está ou não cadastrado. Recebido por
        # injeção (calculado uma vez na composição da aplicação, a partir de um valor
        # aleatório) em vez de ser uma string fixa aqui - uma string no formato de hash
        # bcrypt hardcoded no código dispara falso positivo de "credencial exposta" em
        # SAST (SonarQube), mesmo não sendo segredo de ninguém.
        self._hash_sem_correspondencia = hash_sem_correspondencia

    async def executar(self, entrada: AutenticarUsuarioInput) -> AutenticarUsuarioOutput:
        usuario = await self._usuario_repository.buscar_por_email(entrada.email)
        hash_para_verificar = usuario.senha_hash if usuario else self._hash_sem_correspondencia
        senha_valida = self._password_hasher.verify(entrada.senha, hash_para_verificar)

        if usuario is None or not usuario.ativo or not senha_valida:
            raise CredenciaisInvalidasError

        token = self._token_provider.gerar_token(usuario_id=usuario.id, perfil=usuario.perfil)
        return AutenticarUsuarioOutput(access_token=token)
