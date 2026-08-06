from app.application.servico.dtos import CriarServicoInput, ServicoOutput
from app.application.servico.ports import ServicoRepositoryProtocol
from app.domain.servico.entities import Servico
from app.domain.shared.value_objects import Money


class CriarServicoUseCase:
    def __init__(self, servico_repository: ServicoRepositoryProtocol) -> None:
        self._servico_repository = servico_repository

    async def executar(self, entrada: CriarServicoInput) -> ServicoOutput:
        servico = Servico(
            nome=entrada.nome, descricao=entrada.descricao, preco=Money(valor=entrada.preco)
        )
        criado = await self._servico_repository.criar(servico)

        return ServicoOutput(
            id=criado.id, nome=criado.nome, descricao=criado.descricao, preco=criado.preco.valor
        )
