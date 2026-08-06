from app.domain.servico.exceptions.servico_error import ServicoError


class ServicoNaoEncontradoError(ServicoError):
    def __init__(self, servico_id: int) -> None:
        super().__init__(f"Serviço não encontrado: {servico_id}")
