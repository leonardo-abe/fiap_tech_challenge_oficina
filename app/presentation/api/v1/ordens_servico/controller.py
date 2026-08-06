from app.application.ordem_servico.dtos import (
    CriarOrdemServicoInput,
    ItemPecaInput,
    ItemServicoInput,
)
from app.application.ordem_servico.use_cases import CriarOrdemServicoUseCase
from app.presentation.api.v1.ordens_servico.schemas import (
    OrdemServicoCreateSchema,
    OrdemServicoSchema,
)


class OrdemServicoController:
    def __init__(self, criar_use_case: CriarOrdemServicoUseCase) -> None:
        self._criar_use_case = criar_use_case

    async def criar(self, dados: OrdemServicoCreateSchema) -> OrdemServicoSchema:
        resultado = await self._criar_use_case.executar(
            CriarOrdemServicoInput(
                cliente_id=dados.cliente_id,
                veiculo_id=dados.veiculo_id,
                itens_servico=[
                    ItemServicoInput(servico_id=item.servico_id) for item in dados.itens_servico
                ],
                itens_peca=[
                    ItemPecaInput(peca_id=item.peca_id, quantidade=item.quantidade)
                    for item in dados.itens_peca
                ],
            )
        )
        return OrdemServicoSchema.model_validate(resultado)
