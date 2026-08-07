from app.application.ordem_servico.dtos import (
    ItemPecaOutput,
    ItemServicoOutput,
    OrcamentoOutput,
    OrdemServicoOutput,
)
from app.domain.ordem_servico.entities import OrdemServico


def ordem_servico_to_output(ordem: OrdemServico) -> OrdemServicoOutput:
    orcamento = ordem.calcular_orcamento()

    return OrdemServicoOutput(
        id=ordem.id,
        cliente_id=ordem.cliente_id,
        veiculo_id=ordem.veiculo_id,
        status=ordem.status.value,
        recebida_em=ordem.recebida_em,
        orcamento=OrcamentoOutput(
            total_servicos=orcamento.total_servicos.valor,
            total_pecas=orcamento.total_pecas.valor,
            total=orcamento.total.valor,
        ),
        itens_servico=[
            ItemServicoOutput(servico_id=item.servico_id, nome=item.nome, valor=item.valor.valor)
            for item in ordem.itens_servico
        ],
        itens_peca=[
            ItemPecaOutput(
                peca_id=item.peca_id,
                nome=item.nome,
                quantidade=item.quantidade,
                valor_unitario=item.valor_unitario.valor,
                valor_total=item.valor_total.valor,
            )
            for item in ordem.itens_peca
        ],
    )
