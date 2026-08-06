from app.application.usuario.dtos import CriarUsuarioInput
from app.application.usuario.use_cases import CriarUsuarioUseCase
from app.presentation.api.v1.usuarios.schemas import UsuarioCreateSchema, UsuarioSchema


class UsuarioController:
    def __init__(self, criar_use_case: CriarUsuarioUseCase) -> None:
        self._criar_use_case = criar_use_case

    async def criar(self, dados: UsuarioCreateSchema) -> UsuarioSchema:
        resultado = await self._criar_use_case.executar(
            CriarUsuarioInput(
                nome=dados.nome, email=dados.email, senha=dados.senha, perfil=dados.perfil
            )
        )
        return UsuarioSchema(**vars(resultado))
