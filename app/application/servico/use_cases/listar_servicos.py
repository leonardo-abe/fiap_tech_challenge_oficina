from app.application.servico.dtos import ServicoOutput
from app.application.servico.ports import ServicoRepositoryProtocol


class ListarServicosUseCase:
    def __init__(self, servico_repository: ServicoRepositoryProtocol) -> None:
        self._servico_repository = servico_repository

    async def executar(
        self, nome: str | None = None, limit: int = 50, offset: int = 0
    ) -> list[ServicoOutput]:
        servicos = await self._servico_repository.listar(nome=nome, limit=limit, offset=offset)

        return [
            ServicoOutput(
                id=servico.id,
                nome=servico.nome,
                descricao=servico.descricao,
                preco=servico.preco.valor,
            )
            for servico in servicos
        ]
