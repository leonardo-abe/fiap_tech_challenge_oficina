from dataclasses import replace

from app.domain.cliente.entities import Cliente
from app.domain.ordem_servico.entities import OrdemServico
from app.domain.peca.entities import Peca
from app.domain.peca.exceptions import PecaNaoEncontradaError
from app.domain.servico.entities import Servico
from app.domain.usuario.entities import Usuario
from app.domain.usuario.value_objects import Perfil
from app.domain.veiculo.entities import Veiculo


class FakeClienteRepository:
    def __init__(self) -> None:
        self._clientes: dict[int, Cliente] = {}
        self._proximo_id = 1

    async def criar(self, cliente: Cliente) -> Cliente:
        cliente.id = self._proximo_id
        self._clientes[cliente.id] = cliente
        self._proximo_id += 1
        return cliente

    async def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        return self._clientes.get(cliente_id)

    async def existe_com_documento(self, documento: str) -> bool:
        return any(cliente.documento.valor == documento for cliente in self._clientes.values())

    async def listar(self) -> list[Cliente]:
        return list(self._clientes.values())

    async def atualizar(self, cliente: Cliente) -> Cliente:
        self._clientes[cliente.id] = cliente
        return cliente

    async def remover(self, cliente_id: int) -> None:
        self._clientes.pop(cliente_id, None)


class FakeVeiculoRepository:
    def __init__(self) -> None:
        self._veiculos: dict[int, Veiculo] = {}
        self._proximo_id = 1

    async def criar(self, veiculo: Veiculo) -> Veiculo:
        veiculo.id = self._proximo_id
        self._veiculos[veiculo.id] = veiculo
        self._proximo_id += 1
        return veiculo

    async def buscar_por_id(self, veiculo_id: int) -> Veiculo | None:
        return self._veiculos.get(veiculo_id)

    async def existe_com_placa(self, placa: str) -> bool:
        return any(veiculo.placa.valor == placa for veiculo in self._veiculos.values())

    async def listar(self, cliente_id: int | None = None) -> list[Veiculo]:
        veiculos = list(self._veiculos.values())
        if cliente_id is None:
            return veiculos
        return [veiculo for veiculo in veiculos if veiculo.cliente_id == cliente_id]

    async def atualizar(self, veiculo: Veiculo) -> Veiculo:
        self._veiculos[veiculo.id] = veiculo
        return veiculo

    async def remover(self, veiculo_id: int) -> None:
        self._veiculos.pop(veiculo_id, None)


class FakeServicoRepository:
    def __init__(self) -> None:
        self._servicos: dict[int, Servico] = {}
        self._proximo_id = 1

    async def criar(self, servico: Servico) -> Servico:
        servico.id = self._proximo_id
        self._servicos[servico.id] = servico
        self._proximo_id += 1
        return servico

    async def buscar_por_id(self, servico_id: int) -> Servico | None:
        return self._servicos.get(servico_id)

    async def listar(self) -> list[Servico]:
        return list(self._servicos.values())

    async def atualizar(self, servico: Servico) -> Servico:
        self._servicos[servico.id] = servico
        return servico

    async def remover(self, servico_id: int) -> None:
        self._servicos.pop(servico_id, None)


class FakePecaRepository:
    def __init__(self) -> None:
        self._pecas: dict[int, Peca] = {}
        self._proximo_id = 1

    async def criar(self, peca: Peca) -> Peca:
        peca.id = self._proximo_id
        self._pecas[peca.id] = peca
        self._proximo_id += 1
        return peca

    async def buscar_por_id(self, peca_id: int) -> Peca | None:
        # cópia, não a referência viva do dict - decrementar_estoque/incrementar_estoque
        # simulam um UPDATE atômico direto no "banco", independente de qualquer mutação
        # em memória que o chamador tenha feito na entidade lida (mesma semântica do
        # repositório real, onde ler não afeta o que está persistido até uma escrita).
        peca = self._pecas.get(peca_id)
        return replace(peca) if peca is not None else None

    async def listar(self) -> list[Peca]:
        return list(self._pecas.values())

    async def atualizar(self, peca: Peca) -> Peca:
        self._pecas[peca.id] = peca
        return peca

    async def decrementar_estoque(self, peca_id: int, quantidade: int) -> Peca:
        peca = self._pecas.get(peca_id)
        if peca is None:
            raise PecaNaoEncontradaError(peca_id)
        peca.baixar_estoque(quantidade)
        return peca

    async def incrementar_estoque(self, peca_id: int, quantidade: int) -> Peca:
        peca = self._pecas.get(peca_id)
        if peca is None:
            raise PecaNaoEncontradaError(peca_id)
        peca.repor_estoque(quantidade)
        return peca

    async def remover(self, peca_id: int) -> None:
        self._pecas.pop(peca_id, None)


class FakeOrdemServicoRepository:
    def __init__(self) -> None:
        self._ordens: dict[int, OrdemServico] = {}
        self._proximo_id = 1

    async def criar(self, ordem: OrdemServico) -> OrdemServico:
        ordem.id = self._proximo_id
        self._ordens[ordem.id] = ordem
        self._proximo_id += 1
        return ordem

    async def buscar_por_id(self, ordem_id: int) -> OrdemServico | None:
        return self._ordens.get(ordem_id)

    async def listar(self) -> list[OrdemServico]:
        return list(self._ordens.values())

    async def atualizar(self, ordem: OrdemServico) -> OrdemServico:
        self._ordens[ordem.id] = ordem
        return ordem


class FakeUsuarioRepository:
    def __init__(self) -> None:
        self._usuarios: dict[int, Usuario] = {}
        self._proximo_id = 1

    async def criar(self, usuario: Usuario) -> Usuario:
        usuario.id = self._proximo_id
        self._usuarios[usuario.id] = usuario
        self._proximo_id += 1
        return usuario

    async def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        return self._usuarios.get(usuario_id)

    async def buscar_por_email(self, email: str) -> Usuario | None:
        return next((u for u in self._usuarios.values() if u.email == email), None)

    async def existe_com_email(self, email: str) -> bool:
        return any(usuario.email == email for usuario in self._usuarios.values())


class FakePasswordHasher:
    def hash(self, senha: str) -> str:
        return f"hash({senha})"

    def verify(self, senha: str, senha_hash: str) -> bool:
        return senha_hash == self.hash(senha)


class FakeTokenProvider:
    def __init__(self) -> None:
        self.tokens_gerados: list[tuple[int, Perfil]] = []

    def gerar_token(self, usuario_id: int, perfil: Perfil) -> str:
        self.tokens_gerados.append((usuario_id, perfil))
        return f"token-{usuario_id}-{perfil.value}"
