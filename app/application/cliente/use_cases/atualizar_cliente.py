from app.application.cliente.dtos import AtualizarClienteInput, ClienteOutput
from app.application.cliente.ports import ClienteRepositoryProtocol
from app.domain.cliente.exceptions import ClienteNaoEncontradoError, DocumentoJaCadastradoError
from app.domain.cliente.value_objects import Documento


class AtualizarClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepositoryProtocol) -> None:
        self._cliente_repository = cliente_repository

    async def executar(self, cliente_id: int, entrada: AtualizarClienteInput) -> ClienteOutput:
        cliente = await self._cliente_repository.buscar_por_id(cliente_id)
        if cliente is None:
            raise ClienteNaoEncontradoError(cliente_id)

        documento = Documento(valor=entrada.documento)
        documento_mudou = documento.valor != cliente.documento.valor
        if documento_mudou and await self._cliente_repository.existe_com_documento(
            documento.valor
        ):
            raise DocumentoJaCadastradoError(documento.valor)

        cliente.nome = entrada.nome
        cliente.documento = documento
        cliente.email = entrada.email
        cliente.telefone = entrada.telefone
        atualizado = await self._cliente_repository.atualizar(cliente)

        return ClienteOutput(
            id=atualizado.id,
            nome=atualizado.nome,
            documento=atualizado.documento.valor,
            email=atualizado.email,
            telefone=atualizado.telefone,
        )
