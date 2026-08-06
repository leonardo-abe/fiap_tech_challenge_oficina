from app.application.cliente.dtos import ClienteOutput, CriarClienteInput
from app.application.cliente.ports import ClienteRepositoryProtocol
from app.domain.cliente.entities import Cliente
from app.domain.cliente.exceptions import DocumentoJaCadastradoError
from app.domain.cliente.value_objects import Documento


class CriarClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepositoryProtocol) -> None:
        self._cliente_repository = cliente_repository

    async def executar(self, entrada: CriarClienteInput) -> ClienteOutput:
        documento = Documento(valor=entrada.documento)
        if await self._cliente_repository.existe_com_documento(documento.valor):
            raise DocumentoJaCadastradoError(documento.valor)

        cliente = Cliente(
            nome=entrada.nome, documento=documento, email=entrada.email, telefone=entrada.telefone
        )
        criado = await self._cliente_repository.criar(cliente)

        return ClienteOutput(
            id=criado.id,
            nome=criado.nome,
            documento=criado.documento.valor,
            email=criado.email,
            telefone=criado.telefone,
        )
