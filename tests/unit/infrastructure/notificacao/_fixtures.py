from datetime import UTC, datetime
from decimal import Decimal

from app.application.ordem_servico.dtos import (
    ItemPecaOutput,
    ItemServicoOutput,
    OrcamentoOutput,
    OrdemServicoOutput,
)


def ordem_output_padrao() -> OrdemServicoOutput:
    return OrdemServicoOutput(
        id=42,
        cliente_id=1,
        veiculo_id=1,
        status="AGUARDANDO_APROVACAO",
        recebida_em=datetime.now(UTC),
        orcamento=OrcamentoOutput(
            total_servicos=Decimal("80.00"),
            total_pecas=Decimal("60.00"),
            total=Decimal("140.00"),
        ),
        itens_servico=[
            ItemServicoOutput(servico_id=1, nome="Troca de óleo", valor=Decimal("80.00"))
        ],
        itens_peca=[
            ItemPecaOutput(
                peca_id=1,
                nome="Filtro",
                quantidade=2,
                valor_unitario=Decimal("30.00"),
                valor_total=Decimal("60.00"),
            )
        ],
    )
