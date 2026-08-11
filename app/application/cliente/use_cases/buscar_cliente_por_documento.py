from app.application.cliente.dtos import ClienteOutput
from app.application.cliente.ports import ClienteRepositoryProtocol
from app.domain.cliente.exceptions import ClienteNaoEncontradoError
from app.domain.cliente.value_objects import Documento


class BuscarClientePorDocumentoUseCase:
    def __init__(self, cliente_repository: ClienteRepositoryProtocol) -> None:
        self._cliente_repository = cliente_repository

    async def executar(self, documento: str) -> ClienteOutput:
        documento_valido = Documento(valor=documento)
        cliente = await self._cliente_repository.buscar_por_documento(documento_valido.valor)
        if cliente is None:
            raise ClienteNaoEncontradoError(documento)

        return ClienteOutput(
            id=cliente.id,
            nome=cliente.nome,
            documento=cliente.documento.valor,
            email=cliente.email,
            telefone=cliente.telefone,
        )
