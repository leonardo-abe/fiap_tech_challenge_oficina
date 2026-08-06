from app.domain.peca.exceptions.peca_error import PecaError


class PecaNaoEncontradaError(PecaError):
    def __init__(self, peca_id: int) -> None:
        super().__init__(f"Peça não encontrada: {peca_id}")
