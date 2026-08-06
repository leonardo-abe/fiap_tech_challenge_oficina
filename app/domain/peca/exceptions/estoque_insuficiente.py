from app.domain.peca.exceptions.peca_error import PecaError


class EstoqueInsuficienteError(PecaError):
    def __init__(self, peca_id: int, disponivel: int, solicitado: int) -> None:
        super().__init__(
            f"Estoque insuficiente para a peça {peca_id}: "
            f"disponível {disponivel}, solicitado {solicitado}"
        )
