from app.application.servico.dtos import AtualizarServicoInput, ServicoOutput
from app.application.servico.ports import ServicoRepositoryProtocol
from app.domain.servico.exceptions import ServicoNaoEncontradoError
from app.domain.shared.value_objects import Money


class AtualizarServicoUseCase:
    def __init__(self, servico_repository: ServicoRepositoryProtocol) -> None:
        self._servico_repository = servico_repository

    async def executar(self, servico_id: int, entrada: AtualizarServicoInput) -> ServicoOutput:
        servico = await self._servico_repository.buscar_por_id(servico_id)
        if servico is None:
            raise ServicoNaoEncontradoError(servico_id)

        servico.nome = entrada.nome
        servico.descricao = entrada.descricao
        servico.preco = Money(valor=entrada.preco)
        atualizado = await self._servico_repository.atualizar(servico)

        return ServicoOutput(
            id=atualizado.id,
            nome=atualizado.nome,
            descricao=atualizado.descricao,
            preco=atualizado.preco.valor,
        )
