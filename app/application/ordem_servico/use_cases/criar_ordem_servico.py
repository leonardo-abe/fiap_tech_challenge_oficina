from app.application.cliente.ports import ClienteRepositoryProtocol
from app.application.ordem_servico.dtos import CriarOrdemServicoInput, OrdemServicoOutput
from app.application.ordem_servico.mappers import ordem_servico_to_output
from app.application.ordem_servico.ports import OrdemServicoRepositoryProtocol
from app.application.peca.ports import PecaRepositoryProtocol
from app.application.servico.ports import ServicoRepositoryProtocol
from app.application.veiculo.ports import VeiculoRepositoryProtocol
from app.domain.cliente.exceptions import ClienteNaoEncontradoError
from app.domain.ordem_servico.entities import ItemPeca, ItemServico, OrdemServico
from app.domain.ordem_servico.exceptions import VeiculoNaoPertenceAoClienteError
from app.domain.peca.exceptions import PecaNaoEncontradaError
from app.domain.servico.exceptions import ServicoNaoEncontradoError
from app.domain.veiculo.exceptions import VeiculoNaoEncontradoError


class CriarOrdemServicoUseCase:
    def __init__(
        self,
        ordem_servico_repository: OrdemServicoRepositoryProtocol,
        cliente_repository: ClienteRepositoryProtocol,
        veiculo_repository: VeiculoRepositoryProtocol,
        servico_repository: ServicoRepositoryProtocol,
        peca_repository: PecaRepositoryProtocol,
    ) -> None:
        self._ordem_servico_repository = ordem_servico_repository
        self._cliente_repository = cliente_repository
        self._veiculo_repository = veiculo_repository
        self._servico_repository = servico_repository
        self._peca_repository = peca_repository

    async def executar(self, entrada: CriarOrdemServicoInput) -> OrdemServicoOutput:
        cliente = await self._cliente_repository.buscar_por_id(entrada.cliente_id)
        if cliente is None:
            raise ClienteNaoEncontradoError(entrada.cliente_id)

        veiculo = await self._veiculo_repository.buscar_por_id(entrada.veiculo_id)
        if veiculo is None:
            raise VeiculoNaoEncontradoError(entrada.veiculo_id)
        if veiculo.cliente_id != cliente.id:
            raise VeiculoNaoPertenceAoClienteError(veiculo.id, cliente.id)

        ordem = OrdemServico(cliente_id=cliente.id, veiculo_id=veiculo.id)

        for item_entrada in entrada.itens_servico:
            servico = await self._servico_repository.buscar_por_id(item_entrada.servico_id)
            if servico is None:
                raise ServicoNaoEncontradoError(item_entrada.servico_id)

            ordem.adicionar_item_servico(
                ItemServico(servico_id=servico.id, nome=servico.nome, valor=servico.preco)
            )

        for item_entrada in entrada.itens_peca:
            peca = await self._peca_repository.buscar_por_id(item_entrada.peca_id)
            if peca is None:
                raise PecaNaoEncontradaError(item_entrada.peca_id)

            # a baixa de estoque acontece aqui, orquestrada pelo use case - o agregado
            # OrdemServico nunca muta o agregado Peca diretamente. Toda a request
            # compartilha a mesma sessão (Unit of Work), então se qualquer item
            # subsequente falhar, esta baixa é revertida junto com o resto.
            peca.baixar_estoque(item_entrada.quantidade)
            await self._peca_repository.atualizar(peca)

            ordem.adicionar_item_peca(
                ItemPeca(
                    peca_id=peca.id,
                    nome=peca.nome,
                    quantidade=item_entrada.quantidade,
                    valor_unitario=peca.preco,
                )
            )

        ordem.validar_possui_itens()
        ordem_criada = await self._ordem_servico_repository.criar(ordem)

        return ordem_servico_to_output(ordem_criada)
